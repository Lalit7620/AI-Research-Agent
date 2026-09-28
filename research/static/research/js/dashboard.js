document.addEventListener("DOMContentLoaded", () => {

    const queryInput = document.getElementById("research-query");
    const characterCount = document.getElementById("character-count");
    const researchForm = document.getElementById("research-form");

    const researchButton = document.getElementById("research-button");
    const buttonText = document.getElementById("button-text");
    const buttonIcon = document.getElementById("button-icon");

    const researchStatus = document.getElementById("research-status");
    const statusTitle = document.getElementById("status-title");
    const statusMessage = document.getElementById("status-message");

    const researchResult = document.getElementById("research-result");
    const reportTitle = document.getElementById("report-title");
    const reportContent = document.getElementById("report-content");

    const csrfToken = document.querySelector(
        "[name=csrfmiddlewaretoken]"
    ).value;


    /*
     * Character counter
     */

    if (queryInput && characterCount) {

        queryInput.addEventListener("input", () => {

            characterCount.textContent =
                queryInput.value.length;

        });

    }


    /*
     * Research form
     */

    if (researchForm) {

        researchForm.addEventListener("submit", async (event) => {

            event.preventDefault();


            const query = queryInput.value.trim();


            if (!query) {
                return;
            }


            /*
             * Reset previous result
             */

            researchResult.classList.add("hidden");


            /*
             * Disable button
             */

            researchButton.disabled = true;

            buttonText.textContent = "Researching...";
            buttonIcon.textContent = "⋯";


            /*
             * Show research status
             */

            researchStatus.classList.remove("hidden");

            statusTitle.textContent =
                "Research in progress";

            statusMessage.textContent =
                "Searching the web and analyzing information...";


            try {

                /*
                 * Send research request to Django
                 */

                const response = await fetch(
                    window.location.pathname,
                    {
                        method: "POST",

                        headers: {
                            "Content-Type": "application/json",
                            "X-CSRFToken": csrfToken
                        },

                        credentials: "same-origin",

                        body: JSON.stringify({
                            query: query
                        })
                    }
                );


                /*
                 * Convert response to JSON
                 */

                const data = await response.json();


                /*
                 * Handle backend errors
                 */

                if (!response.ok) {

                    throw new Error(
                        data.error ||
                        data.detail ||
                        "Research request failed."
                    );

                }


                /*
                 * Research completed
                 */

                statusTitle.textContent =
                    "Research completed";

                statusMessage.textContent =
                    "Your research report is ready.";


                /*
                 * Display report
                 */

                reportTitle.textContent =
                    data.query;

                reportContent.textContent =
                    data.report;

                researchResult.classList.remove("hidden");


                /*
                 * Update recent research section
                 */

                const recentResearch =
                    document.getElementById("recent-research");

                if (recentResearch) {

                    recentResearch.innerHTML = `
                        <div class="text-4xl mb-4">
                            ✓
                        </div>

                        <h4 class="font-medium text-lg">
                            Research completed
                        </h4>

                        <p class="text-slate-500 text-sm mt-2">
                            Your latest research report is ready above.
                        </p>
                    `;

                }

            }

            catch (error) {

                console.error(
                    "Research error:",
                    error
                );


                statusTitle.textContent =
                    "Research failed";

                statusMessage.textContent =
                    error.message;


                researchResult.classList.add("hidden");

            }

            finally {

                /*
                 * Re-enable button
                 */

                researchButton.disabled = false;

                buttonText.textContent =
                    "Start Research";

                buttonIcon.textContent =
                    "✦";

            }

        });

    }

});