from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import render

from .models import ResearchRequest, ResearchReport
from .serializers import ResearchRequestSerializers,ResearchHistorySerializers,ResearchReportSerializer
from .agent.agent import ResearchAgent


class ResearchView(APIView):

    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        return render(
            request,
            "research/dashboard.html"
        )

    def post(self, request):

        serializer = ResearchRequestSerializers(
            data=request.data
        )

        if not serializer.is_valid():

            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        research_request = serializer.save(
            user=request.user
        )

        research_request.status = "RESEARCHING"
        research_request.save()

        try:

            agent = ResearchAgent(
                user_id=request.user.id
            )

            result = agent.run(
                research_request.query
            )

            ResearchReport.objects.create(
                research_request=research_request,
                content=result
            )

            research_request.status = "COMPLETED"
            research_request.save()

            return Response(
                {
                    "id": research_request.id,
                    "status": research_request.status,
                    "query": research_request.query,
                    "report": result,
                },
                status=status.HTTP_201_CREATED
            )

        except Exception as e:

            research_request.status = "FAILED"
            research_request.save()

            return Response(
                {
                    "id": research_request.id,
                    "status": research_request.status,
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
            
class ResearchHistoryView(APIView):
    authentication_classes=[SessionAuthentication]
    permission_classes=[IsAuthenticated]
    
    def get(self,request):
        research_requests=ResearchRequest.objects.filter(
            user=request.user
        ).order_by("-created_at")
        
        serializer=ResearchHistorySerializers(
            research_requests,
            many=True
        )
        
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )
        
class ResearchDetailView(APIView):

    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, request_id):

        research_request = ResearchRequest.objects.filter(
            id=request_id,
            user=request.user
        ).first()

        if not research_request:

            return Response(
                {
                    "error": "Research request not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if not hasattr(research_request, "report"):

            return Response(
                {
                    "error": "Research report not available."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        report = research_request.report

        return Response(
            {
                "id": research_request.id,
                "query": research_request.query,
                "status": research_request.status,
                "report": ResearchReportSerializer(
                    report
                ).data
            },
            status=status.HTTP_200_OK
        )