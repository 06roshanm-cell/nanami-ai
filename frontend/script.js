const API = "http://127.0.0.1:8000";

let sentimentChart = null;
let categoryChart = null;


/* =========================================================
   LOGIN
========================================================= */

function setupLogin() {

    const loginScreen =
        document.getElementById("loginScreen");

    const app =
        document.getElementById("app");

    const loginForm =
        document.getElementById("loginForm");

    const logoutButton =
        document.getElementById("logoutButton");


    if (!loginForm) {
        return;
    }


    if (
        sessionStorage.getItem(
            "nanami_logged_in"
        ) === "true"
    ) {

        loginScreen.classList.add("hidden");

        app.classList.remove("hidden");

        loadDashboard();

        loadTimeline();
    }


    loginForm.addEventListener(
        "submit",
        function (event) {

            event.preventDefault();


            const email =
                document
                    .getElementById("loginEmail")
                    .value
                    .trim();


            const password =
                document
                    .getElementById("loginPassword")
                    .value
                    .trim();


            if (!email || !password) {

                alert(
                    "Please enter email and password."
                );

                return;
            }


            sessionStorage.setItem(
                "nanami_logged_in",
                "true"
            );


            loginScreen.classList.add(
                "hidden"
            );

            app.classList.remove(
                "hidden"
            );


            loadDashboard();

            loadTimeline();
        }
    );


    if (logoutButton) {

        logoutButton.addEventListener(
            "click",
            function () {

                sessionStorage.removeItem(
                    "nanami_logged_in"
                );


                app.classList.add(
                    "hidden"
                );

                loginScreen.classList.remove(
                    "hidden"
                );


                loginForm.reset();
            }
        );
    }
}


/* =========================================================
   NAVIGATION
========================================================= */

function setupNavigation() {

    const navItems =
        document.querySelectorAll(
            ".nav-item"
        );


    navItems.forEach(item => {

        item.addEventListener(
            "click",
            function () {

                navItems.forEach(nav => {

                    nav.classList.remove(
                        "active"
                    );
                });


                this.classList.add(
                    "active"
                );


                const target =
                    this.getAttribute(
                        "data-target"
                    );


                if (!target) {
                    return;
                }


                const section =
                    document.getElementById(
                        target
                    );


                if (section) {

                    section.scrollIntoView({
                        behavior: "smooth",
                        block: "start"
                    });
                }
            }
        );
    });
}


/* =========================================================
   DASHBOARD
========================================================= */

async function loadDashboard() {

    try {

        const response =
            await fetch(
                `${API}/dashboard`
            );


        if (!response.ok) {

            throw new Error(
                `Dashboard request failed: ${response.status}`
            );
        }


        const data =
            await response.json();


        console.log(
            "Nanami dashboard:",
            data
        );


        /* KPI */

        setText(
            "total",
            data.total_feedback ?? 0
        );


        setText(
            "positive",
            data.positive ?? 0
        );


        setText(
            "negative",
            data.negative ?? 0
        );


        setText(
            "rating",
            data.average_rating ?? 0
        );


        /* Insights */

        setText(
            "positiveInsight",
            data.positive ?? 0
        );


        setText(
            "negativeInsight",
            data.negative ?? 0
        );


        /* Charts */

        createSentimentChart(data);

        createCategoryChart(data);


    } catch (error) {

        console.error(
            "Dashboard error:",
            error
        );


        setText(
            "total",
            "—"
        );

        setText(
            "positive",
            "—"
        );

        setText(
            "negative",
            "—"
        );

        setText(
            "rating",
            "—"
        );
    }
}


/* =========================================================
   SENTIMENT CHART
========================================================= */

function createSentimentChart(data) {

    const canvas =
        document.getElementById(
            "sentimentChart"
        );


    if (!canvas) {
        return;
    }


    if (sentimentChart) {

        sentimentChart.destroy();

        sentimentChart = null;
    }


    sentimentChart =
        new Chart(
            canvas,
            {

                type: "doughnut",

                data: {

                    labels: [
                        "Positive",
                        "Negative",
                        "Neutral"
                    ],

                    datasets: [
                        {

                            data: [
                                data.positive ?? 0,
                                data.negative ?? 0,
                                data.neutral ?? 0
                            ],

                            backgroundColor: [
                                "#34D399",
                                "#FB7185",
                                "#FBBF24"
                            ],

                            borderColor:
                                "#101827",

                            borderWidth: 5,

                            hoverOffset: 8
                        }
                    ]
                },


                options: {

                    responsive: true,

                    maintainAspectRatio: false,

                    cutout: "72%",


                    plugins: {

                        legend: {

                            position: "bottom",

                            labels: {

                                color:
                                    "#CBD5E1",

                                usePointStyle:
                                    true,

                                pointStyle:
                                    "circle",

                                padding: 18,

                                font: {
                                    size: 11
                                }
                            }
                        }
                    }
                }
            }
        );
}


/* =========================================================
   CATEGORY CHART
========================================================= */

function createCategoryChart(data) {

    const canvas =
        document.getElementById(
            "categoryChart"
        );


    if (!canvas) {
        return;
    }


    if (categoryChart) {

        categoryChart.destroy();

        categoryChart = null;
    }


    categoryChart =
        new Chart(
            canvas,
            {

                type: "bar",

                data: {

                    labels: [
                        "Battery",
                        "Camera",
                        "Heating",
                        "WiFi"
                    ],

                    datasets: [
                        {

                            label:
                                "Customer reports",

                            data: [
                                data.battery ?? 0,
                                data.camera ?? 0,
                                data.heating ?? 0,
                                data.wifi ?? 0
                            ],

                            backgroundColor: [
                                "#8B5CF6",
                                "#22D3EE",
                                "#FBBF24",
                                "#EC4899"
                            ],

                            borderRadius: 10,

                            borderSkipped:
                                false
                        }
                    ]
                },


                options: {

                    responsive: true,

                    maintainAspectRatio:
                        false,


                    plugins: {

                        legend: {
                            display: false
                        }
                    },


                    scales: {

                        x: {

                            grid: {
                                display: false
                            },

                            ticks: {

                                color:
                                    "#94A3B8",

                                font: {
                                    size: 10
                                }
                            }
                        },


                        y: {

                            beginAtZero:
                                true,

                            grid: {

                                color:
                                    "rgba(148,163,184,0.09)"
                            },

                            ticks: {

                                color:
                                    "#94A3B8",

                                font: {
                                    size: 10
                                }
                            }
                        }
                    }
                }
            }
        );
}


/* =========================================================
   HINDSIGHT MEMORY
========================================================= */

async function loadTimeline() {

    const timeline =
        document.getElementById(
            "timeline"
        );


    if (!timeline) {
        return;
    }


    try {

        const response =
            await fetch(
                `${API}/timeline`
            );


        if (!response.ok) {

            throw new Error(
                `Timeline request failed: ${response.status}`
            );
        }


        const data =
            await response.json();


        timeline.innerHTML = "";


        if (
            !Array.isArray(data) ||
            data.length === 0
        ) {

            timeline.innerHTML = `

                <div class="memory-loading">
                    No Hindsight memories available yet.
                </div>

            `;

            return;
        }


        data.forEach(item => {

            const memory =
                document.createElement(
                    "div"
                );


            memory.className =
                "memory-item";


            memory.innerHTML = `

                <div class="memory-dot"></div>

                <div class="memory-content">

                    <h3>
                        ${escapeHtml(
                            item.issue
                        )}
                    </h3>

                    <p>
                        ${escapeHtml(
                            item.solution
                        )}
                    </p>

                    <span class="memory-success">

                        Success rate:
                        ${item.success ?? 0}%

                    </span>

                </div>

            `;


            timeline.appendChild(
                memory
            );
        });


    } catch (error) {

        console.error(
            "Timeline error:",
            error
        );


        timeline.innerHTML = `

            <div class="memory-loading">

                Unable to load Hindsight memory.

            </div>

        `;
    }
}


/* =========================================================
   CHAT
========================================================= */

function setupChat() {

    const form =
        document.getElementById(
            "chatForm"
        );


    const input =
        document.getElementById(
            "question"
        );


    if (!form || !input) {
        return;
    }


    form.addEventListener(
        "submit",
        function (event) {

            event.preventDefault();

            analyzeFeedback();
        }
    );


    input.addEventListener(
        "keydown",
        function (event) {

            if (
                event.key === "Enter" &&
                !event.shiftKey
            ) {

                event.preventDefault();

                analyzeFeedback();
            }
        }
    );


    input.addEventListener(
        "input",
        function () {

            this.style.height =
                "auto";


            this.style.height =
                Math.min(
                    this.scrollHeight,
                    140
                ) + "px";
        }
    );
}


/* =========================================================
   SUGGESTION
========================================================= */

function useSuggestion(button) {

    const input =
        document.getElementById(
            "question"
        );


    if (!input || !button) {
        return;
    }


    input.value =
        button.innerText;


    input.focus();


    input.style.height =
        "auto";


    input.style.height =
        Math.min(
            input.scrollHeight,
            140
        ) + "px";
}


/* =========================================================
   ANALYZE
========================================================= */

async function analyzeFeedback() {

    const input =
        document.getElementById(
            "question"
        );


    if (!input) {
        return;
    }


    const question =
        input.value.trim();


    if (!question) {

        input.focus();

        return;
    }


    addUserMessage(
        question
    );


    input.value = "";

    input.style.height =
        "auto";


    const sendButton =
        document.getElementById(
            "sendButton"
        );


    if (sendButton) {

        sendButton.disabled =
            true;


        const text =
            sendButton.querySelector(
                "span"
            );


        if (text) {

            text.innerText =
                "Analyzing...";
        }
    }


    addTypingMessage();


    try {

        const response =
            await fetch(
                `${API}/multi-agent`,
                {

                    method:
                        "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify({
                            question:
                                question
                        })
                }
            );


        if (!response.ok) {

            throw new Error(
                `Server returned ${response.status}`
            );
        }


        const data =
            await response.json();


        console.log(
            "Nanami AI response:",
            data
        );


        removeTypingMessage();


        addAIMessage(
            buildAIResponse(data)
        );


        displayAnalysis(
            data
        );


    } catch (error) {

        console.error(
            "AI analysis error:",
            error
        );


        removeTypingMessage();


        addAIMessage(`

            <strong>
                Connection problem
            </strong>

            <br><br>

            Nanami AI could not connect
            to the backend.

            <br><br>

            Make sure FastAPI is running at:

            <br><br>

            <strong>
                http://127.0.0.1:8000
            </strong>

        `);


    } finally {

        if (sendButton) {

            sendButton.disabled =
                false;


            const text =
                sendButton.querySelector(
                    "span"
                );


            if (text) {

                text.innerText =
                    "Analyze";
            }
        }
    }
}


/* =========================================================
   AI RESPONSE
========================================================= */

function buildAIResponse(data) {

    const sentiment =
        data.sentiment ||
        "Unknown";


    const rootCause =
        data.root_cause ||
        "Not detected";


    const recommendation =
        data.recommendation ||
        "No recommendation";


    return `

        <strong>
            Analysis completed
        </strong>

        <br><br>

        <strong>
            Sentiment:
        </strong>

        ${escapeHtml(
            sentiment
        )}

        <br>

        <strong>
            Root cause:
        </strong>

        ${escapeHtml(
            rootCause
        )}

        <br>

        <strong>
            Recommendation:
        </strong>

        ${escapeHtml(
            recommendation
        )}

    `;
}


/* =========================================================
   ANALYSIS PANEL
========================================================= */

function displayAnalysis(data) {

    const panel =
        document.getElementById(
            "analysisPanel"
        );


    if (!panel) {
        return;
    }


    panel.classList.remove(
        "hidden"
    );


    setText(
        "ragOutput",
        data.context ||
        "No relevant customer evidence found."
    );


    setText(
        "sentimentOutput",
        data.sentiment ||
        "Unknown"
    );


    setText(
        "rootOutput",
        data.root_cause ||
        "Not detected"
    );


    setText(
        "recommendOutput",
        data.recommendation ||
        "No recommendation"
    );


    setTimeout(
        function () {

            panel.scrollIntoView({
                behavior:
                    "smooth",

                block:
                    "nearest"
            });

        },
        100
    );
}


/* =========================================================
   USER MESSAGE
========================================================= */

function addUserMessage(text) {

    const container =
        document.getElementById(
            "chatMessages"
        );


    if (!container) {
        return;
    }


    const message =
        document.createElement(
            "div"
        );


    message.className =
        "message user-message";


    message.innerHTML = `

        <div class="message-content">

            <div class="message-name">
                You
            </div>

            <p>
                ${escapeHtml(text)}
            </p>

        </div>

        <div class="message-avatar user-avatar">
            Y
        </div>

    `;


    container.appendChild(
        message
    );


    scrollChat();
}


/* =========================================================
   AI MESSAGE
========================================================= */

function addAIMessage(html) {

    const container =
        document.getElementById(
            "chatMessages"
        );


    if (!container) {
        return;
    }


    const message =
        document.createElement(
            "div"
        );


    message.className =
        "message ai-message";


    message.innerHTML = `

        <div class="message-avatar ai-avatar">
            N
        </div>

        <div class="message-content">

            <div class="message-name">
                Nanami AI
            </div>

            <p>
                ${html}
            </p>

        </div>

    `;


    container.appendChild(
        message
    );


    scrollChat();
}


/* =========================================================
   TYPING
========================================================= */

function addTypingMessage() {

    const container =
        document.getElementById(
            "chatMessages"
        );


    if (!container) {
        return;
    }


    const message =
        document.createElement(
            "div"
        );


    message.id =
        "typingMessage";


    message.className =
        "message ai-message";


    message.innerHTML = `

        <div class="message-avatar ai-avatar">
            N
        </div>

        <div class="message-content">

            <div class="message-name">
                Nanami AI
            </div>

            <p>
                Analyzing customer feedback
                <span class="typing-dots">
                    • • •
                </span>
            </p>

        </div>

    `;


    container.appendChild(
        message
    );


    scrollChat();
}


/* =========================================================
   REMOVE TYPING
========================================================= */

function removeTypingMessage() {

    const message =
        document.getElementById(
            "typingMessage"
        );


    if (message) {
        message.remove();
    }
}


/* =========================================================
   CHAT SCROLL
========================================================= */

function scrollChat() {

    const container =
        document.getElementById(
            "chatMessages"
        );


    if (!container) {
        return;
    }


    container.scrollTop =
        container.scrollHeight;
}


/* =========================================================
   SET TEXT
========================================================= */

function setText(
    id,
    value
) {

    const element =
        document.getElementById(
            id
        );


    if (element) {

        element.innerText =
            value;
    }
}


/* =========================================================
   HTML ESCAPE
========================================================= */

function escapeHtml(value) {

    if (
        value === null ||
        value === undefined
    ) {

        return "";
    }


    return String(value)

        .replace(
            /&/g,
            "&amp;"
        )

        .replace(
            /</g,
            "&lt;"
        )

        .replace(
            />/g,
            "&gt;"
        )

        .replace(
            /"/g,
            "&quot;"
        )

        .replace(
            /'/g,
            "&#039;"
        );
}


/* =========================================================
   START
========================================================= */

window.addEventListener(
    "DOMContentLoaded",
    function () {

        setupLogin();

        setupNavigation();

        setupChat();

    }
);