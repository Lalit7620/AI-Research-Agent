from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import render

from .models import ResearchRequest, ResearchReport
from .serializers import ResearchRequestSerializers
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

            agent = ResearchAgent()

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