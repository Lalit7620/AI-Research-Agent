document.addEventListener("DOMContentLoaded", () => {

    const uploadForm =
        document.getElementById("document-upload-form");

    const fileInput =
        document.getElementById("document-file");

    const uploadButton =
        document.getElementById("upload-button");

    const uploadButtonText =
        document.getElementById("upload-button-text");

    const uploadMessage =
        document.getElementById("upload-message");

    const documentsList =
        document.getElementById("documents-list");

    const csrfToken =
        document.querySelector(
            "[name=csrfmiddlewaretoken]"
        ).value;


    /*
     * Show upload message
     */

    function showUploadMessage(message, success) {

        uploadMessage.textContent = message;

        uploadMessage.classList.remove(
            "hidden",
            "text-emerald-400",
            "text-red-400"
        );

        if (success) {

            uploadMessage.classList.add(
                "text-emerald-400"
            );

        } else {

            uploadMessage.classList.add(
                "text-red-400"
            );

        }

    }


    /*
     * Load documents
     */

    async function loadDocuments() {

        try {

            const response = await fetch(
                "/api/documents/",
                {
                    method: "GET",
                    credentials: "same-origin"
                }
            );


            const data =
                await response.json();


            if (!response.ok) {

                throw new Error(
                    data.detail ||
                    "Failed to load documents."
                );

            }


            /*
             * No documents
             */

            if (data.length === 0) {

                documentsList.innerHTML = `
                    <div class="text-center py-8">

                        <div class="text-4xl mb-4">
                            📄
                        </div>

                        <h4 class="font-medium text-lg">
                            No documents yet
                        </h4>

                        <p class="text-slate-500 text-sm mt-2">
                            Upload a PDF to add it to your knowledge base.
                        </p>

                    </div>
                `;

                return;

            }


            /*
             * Clear loading state
             */

            documentsList.innerHTML = "";


            /*
             * Create document items
             */

            data.forEach((documentData) => {

                const documentItem =
                    document.createElement("div");

                documentItem.className =
                    "flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-slate-800 py-5 last:border-b-0";


                /*
                 * Document information
                 */

                const information =
                    document.createElement("div");


                const filename =
                    documentData.file
                        .split("/")
                        .pop();


                const filenameElement =
                    document.createElement("p");

                filenameElement.className =
                    "text-slate-200 font-medium";

                filenameElement.textContent =
                    `📄 ${filename}`;


                const dateElement =
                    document.createElement("p");

                dateElement.className =
                    "text-xs text-slate-500 mt-2";

                dateElement.textContent =
                    `Uploaded ${new Date(
                        documentData.uploaded_at
                    ).toLocaleString()}`;


                information.appendChild(
                    filenameElement
                );

                information.appendChild(
                    dateElement
                );


                /*
                 * Delete button
                 */

                const deleteButton =
                    document.createElement("button");

                deleteButton.type =
                    "button";

                deleteButton.textContent =
                    "Delete";

                deleteButton.className =
                    "text-sm text-red-400 hover:text-red-300 transition";


                deleteButton.addEventListener(
                    "click",
                    () => deleteDocument(
                        documentData.id
                    )
                );


                documentItem.appendChild(
                    information
                );

                documentItem.appendChild(
                    deleteButton
                );


                documentsList.appendChild(
                    documentItem
                );

            });

        }

        catch (error) {

            console.error(
                "Document loading error:",
                error
            );


            documentsList.innerHTML = `
                <div class="text-center py-8">

                    <p class="text-red-400">
                        Unable to load documents.
                    </p>

                </div>
            `;

        }

    }


    /*
     * Delete document
     */

    async function deleteDocument(documentId) {

        const confirmed =
            confirm(
                "Are you sure you want to delete this document?"
            );


        if (!confirmed) {
            return;
        }


        try {

            const response = await fetch(
                `/api/documents/${documentId}/`,
                {
                    method: "DELETE",

                    headers: {
                        "X-CSRFToken":
                            csrfToken
                    },

                    credentials:
                        "same-origin"
                }
            );


            if (!response.ok) {

                const data =
                    await response.json();

                throw new Error(
                    data.detail ||
                    "Failed to delete document."
                );

            }


            /*
             * Refresh list
             */

            await loadDocuments();

        }

        catch (error) {

            console.error(
                "Document deletion error:",
                error
            );

            alert(
                error.message
            );

        }

    }


    /*
     * Upload document
     */

    if (uploadForm) {

        uploadForm.addEventListener(
            "submit",
            async (event) => {

                event.preventDefault();


                /*
                 * Check file
                 */

                if (!fileInput.files.length) {

                    showUploadMessage(
                        "Please select a PDF.",
                        false
                    );

                    return;

                }


                const file =
                    fileInput.files[0];


                /*
                 * Check PDF type
                 */

                if (
                    file.type !==
                    "application/pdf"
                ) {

                    showUploadMessage(
                        "Only PDF files are allowed.",
                        false
                    );

                    return;

                }


                /*
                 * Create multipart form data
                 */

                const formData =
                    new FormData();

                formData.append(
                    "file",
                    file
                );


                /*
                 * Disable button
                 */

                uploadButton.disabled =
                    true;

                uploadButtonText.textContent =
                    "Uploading...";


                try {

                    const response =
                        await fetch(
                            "/api/documents/upload/",
                            {
                                method: "POST",

                                headers: {
                                    "X-CSRFToken":
                                        csrfToken
                                },

                                credentials:
                                    "same-origin",

                                body:
                                    formData
                            }
                        );


                    const data =
                        await response.json();


                    if (!response.ok) {

                        throw new Error(
                            data.detail ||
                            "Document upload failed."
                        );

                    }


                    showUploadMessage(
                        "Document uploaded successfully.",
                        true
                    );


                    /*
                     * Clear file input
                     */

                    fileInput.value = "";


                    /*
                     * Refresh document list
                     */

                    await loadDocuments();

                }

                catch (error) {

                    console.error(
                        "Document upload error:",
                        error
                    );


                    showUploadMessage(
                        error.message,
                        false
                    );

                }

                finally {

                    uploadButton.disabled =
                        false;

                    uploadButtonText.textContent =
                        "Upload Document";

                }

            }
        );

    }


    /*
     * Load documents when page opens
     */

    loadDocuments();

});