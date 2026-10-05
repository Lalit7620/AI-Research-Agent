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

    const recentResearch =
        document.getElementById("recent-research");

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
     * Display a saved research report
     */

    async function openResearchReport(requestId) {

        try {

            researchStatus.classList.remove("hidden");

            statusTitle.textContent =
                "Loading research";

            statusMessage.textContent =
                "Retrieving your saved research report...";


            const response = await fetch(
                `/api/research/${requestId}/`,
                {
                    method: "GET",
                    credentials: "same-origin"
                }
            );


            const data = await response.json();


            if (!response.ok) {

                throw new Error(
                    data.error ||
                    data.detail ||
                    "Failed to load research report."
                );

            }


            /*
             * Display saved report
             */

            reportTitle.textContent =
                data.query;


            const renderedReport =
                marked.parse(
                    data.report.content
                );


            reportContent.innerHTML =
                DOMPurify.sanitize(
                    renderedReport
                );


            researchResult.classList.remove(
                "hidden"
            );


            statusTitle.textContent =
                "Research loaded";

            statusMessage.textContent =
                "Saved research report loaded successfully.";


            /*
             * Scroll to report
             */

            researchResult.scrollIntoView({
                behavior: "smooth",
                block: "start"
            });

        }

        catch (error) {

            console.error(
                "Report loading error:",
                error
            );


            statusTitle.textContent =
                "Unable to load research";

            statusMessage.textContent =
                error.message;

        }

    }


    /*
     * Load research history
     */

    async function loadResearchHistory() {

        if (!recentResearch) {
            return;
        }

        try {

            const response = await fetch(
                "/api/research/history/",
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
                    "Failed to load research history."
                );

            }


            /*
             * No research history
             */

            if (data.length === 0) {

                recentResearch.innerHTML = `
                    <div class="text-center py-6">

                        <div class="text-4xl mb-4">
                            ✦
                        </div>

                        <h4 class="font-medium text-lg">
                            No research yet
                        </h4>

                        <p class="text-slate-500 text-sm mt-2">
                            Your completed research will appear here.
                        </p>

                    </div>
                `;

                return;
            }


            /*
             * Clear loading state
             */

            recentResearch.innerHTML = "";


            /*
             * Display history
             */

            data.slice(0, 10).forEach((research) => {

                const researchItem =
                    document.createElement("button");


                researchItem.type =
                    "button";


                researchItem.className =
                    "w-full text-left border-b border-slate-800 py-5 last:border-b-0 hover:bg-slate-900/50 transition rounded-lg px-3";


                /*
                 * Query
                 */

                const query =
                    document.createElement("p");

                query.className =
                    "text-slate-200 font-medium";

                query.textContent =
                    research.query;


                /*
                 * Metadata
                 */

                const metadata =
                    document.createElement("div");

                metadata.className =
                    "flex flex-wrap items-center gap-3 mt-2";


                /*
                 * Status
                 */

                const status =
                    document.createElement("span");

                status.className =
                    "text-xs font-medium px-2 py-1 rounded-full";


                if (research.status === "COMPLETED") {

                    status.classList.add(
                        "bg-emerald-500/10",
                        "text-emerald-400"
                    );

                }

                else if (research.status === "FAILED") {

                    status.classList.add(
                        "bg-red-500/10",
                        "text-red-400"
                    );

                }

                else {

                    status.classList.add(
                        "bg-yellow-500/10",
                        "text-yellow-400"
                    );

                }


                status.textContent =
                    research.status;


                /*
                 * Date
                 */

                const date =
                    document.createElement("span");

                date.className =
                    "text-xs text-slate-500";

                date.textContent =
                    new Date(
                        research.created_at
                    ).toLocaleString();


                metadata.appendChild(status);
                metadata.appendChild(date);


                researchItem.appendChild(query);
                researchItem.appendChild(metadata);


                /*
                 * Open saved report when clicked
                 */

                researchItem.addEventListener(
                    "click",
                    () => {

                        if (
                            research.status ===
                            "COMPLETED"
                        ) {

                            openResearchReport(
                                research.id
                            );

                        }

                    }
                );


                recentResearch.appendChild(
                    researchItem
                );

            });

        }

        catch (error) {

            console.error(
                "History error:",
                error
            );


            recentResearch.innerHTML = `
                <div class="text-center py-6">

                    <p class="text-red-400">
                        Unable to load research history.
                    </p>

                </div>
            `;

        }

    }


    /*
     * Load history when dashboard opens
     */

    loadResearchHistory();


    /*
     * Research form
     */

    if (researchForm) {

        researchForm.addEventListener(
            "submit",
            async (event) => {

                event.preventDefault();


                const query =
                    queryInput.value.trim();


                if (!query) {
                    return;
                }


                /*
                 * Reset previous result
                 */

                researchResult.classList.add(
                    "hidden"
                );


                /*
                 * Disable button
                 */

                researchButton.disabled =
                    true;

                buttonText.textContent =
                    "Researching...";

                buttonIcon.textContent =
                    "⋯";


                /*
                 * Show research status
                 */

                researchStatus.classList.remove(
                    "hidden"
                );

                statusTitle.textContent =
                    "Research in progress";

                statusMessage.textContent =
                    "Searching the web and analyzing information...";


                try {

                    /*
                     * Send research request
                     */

                    const response = await fetch(
                        window.location.pathname,
                        {
                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json",

                                "X-CSRFToken":
                                    csrfToken
                            },

                            credentials:
                                "same-origin",

                            body: JSON.stringify({
                                query: query
                            })
                        }
                    );


                    /*
                     * Convert response to JSON
                     */

                    const data =
                        await response.json();


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


                    const renderedReport =
                        marked.parse(
                            data.report
                        );


                    reportContent.innerHTML =
                        DOMPurify.sanitize(
                            renderedReport
                        );


                    researchResult.classList.remove(
                        "hidden"
                    );


                    /*
                     * Refresh history
                     */

                    loadResearchHistory();

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


                    researchResult.classList.add(
                        "hidden"
                    );

                }

                finally {

                    /*
                     * Re-enable button
                     */

                    researchButton.disabled =
                        false;

                    buttonText.textContent =
                        "Start Research";

                    buttonIcon.textContent =
                        "✦";

                }

            }
        );

    }

});