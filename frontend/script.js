// ============================================================
// PayShield AI - Complete Frontend JavaScript
// Matches the current index.html
// ============================================================


// ============================================================
// TEST DATA
// ============================================================

const legitimateData = {
    time: 0,
    amount: 149.62,

    V1: 1.072,
    V2: -0.343,
    V3: 1.001,
    V4: 1.380,
    V5: -0.344,
    V6: 0.462,
    V7: -0.089,
    V8: 0.304,
    V9: 0.348,
    V10: 0.089,
    V11: 0.172,
    V12: 0.134,
    V13: 0.514,
    V14: -0.451,
    V15: 1.001,
    V16: -0.443,
    V17: 0.008,
    V18: -0.139,
    V19: 0.016,
    V20: 0.012,
    V21: -0.018,
    V22: -0.103,
    V23: -0.113,
    V24: 0.062,
    V25: 0.129,
    V26: -0.189,
    V27: 0.021,
    V28: 0.012
};


const fraudData = {
    time: 406,
    amount: 0,

    V1: -2.312227,
    V2: 1.951992,
    V3: -1.609851,
    V4: 3.997906,
    V5: -0.522188,
    V6: -1.426545,
    V7: -2.537387,
    V8: 1.391657,
    V9: -2.770089,
    V10: -2.772272,
    V11: 3.202033,
    V12: -2.899907,
    V13: -0.595222,
    V14: -4.289254,
    V15: 0.389724,
    V16: -1.140747,
    V17: -2.830056,
    V18: -0.016822,
    V19: 0.416956,
    V20: 0.126911,
    V21: 0.517232,
    V22: -0.035049,
    V23: -0.465211,
    V24: 0.320198,
    V25: 0.044519,
    V26: 0.177840,
    V27: 0.261145,
    V28: -0.143276
};


// ============================================================
// ELEMENTS
// ============================================================

const featuresContainer = document.getElementById("features");

const analyzeButton = document.getElementById("analyzeBtn");

const loadingElement = document.getElementById("loading");

const shieldElement = document.getElementById("shield");

const resultTitleElement = document.getElementById("resultTitle");

const resultSubtitleElement = document.getElementById("resultSubtitle");

const probabilityElement = document.getElementById("probability");

const riskPillElement = document.getElementById("riskPill");

const recommendationElement = document.getElementById("recommendation");

const historyBody = document.getElementById("historyBody");

const totalTransactionsElement =
    document.getElementById("totalTransactions");

const fraudCountElement =
    document.getElementById("fraudCount");

const legitimateCountElement =
    document.getElementById("legitimateCount");

const fraudRateElement =
    document.getElementById("fraudRate");


// ============================================================
// CREATE V1 - V28 INPUTS
// ============================================================

if (featuresContainer) {

    featuresContainer.innerHTML = "";

    for (let i = 1; i <= 28; i++) {

        const field = document.createElement("div");

        field.className = "field";

        field.innerHTML = `
            <label>V${i}</label>

            <input
                type="number"
                step="any"
                id="V${i}"
                placeholder="0"
            >
        `;

        featuresContainer.appendChild(field);
    }
}


// ============================================================
// LOAD DATA INTO FORM
// ============================================================

function loadData(data) {

    document.getElementById("time").value = data.time;

    document.getElementById("amount").value = data.amount;

    for (let i = 1; i <= 28; i++) {

        const input = document.getElementById(`V${i}`);

        if (input) {
            input.value = data[`V${i}`];
        }
    }

}


// ============================================================
// LOAD LEGITIMATE TEST
// ============================================================

function loadLegitimate() {

    loadData(legitimateData);

    resetResult();

}


// ============================================================
// LOAD FRAUD TEST
// ============================================================

function loadFraud() {

    loadData(fraudData);

    resetResult();

}


// ============================================================
// RESET RESULT
// ============================================================

function resetResult() {

    shieldElement.textContent = "🛡️";

    shieldElement.style.background =
        "rgba(34,197,94,0.10)";

    shieldElement.style.borderColor =
        "rgba(34,197,94,0.2)";

    resultTitleElement.textContent =
        "Awaiting Analysis";

    resultSubtitleElement.textContent =
        "Submit a transaction to receive a risk assessment.";

    probabilityElement.textContent = "—";

    riskPillElement.textContent =
        "NO ASSESSMENT";

    riskPillElement.style.color =
        "#86efac";

    riskPillElement.style.background =
        "rgba(34,197,94,0.12)";

    recommendationElement.textContent =
        "Your transaction analysis will appear here after you submit the required transaction details.";

}


// ============================================================
// GET HISTORY
// ============================================================

function getHistory() {

    try {

        return JSON.parse(
            localStorage.getItem("payshield_history")
        ) || [];

    } catch (error) {

        return [];

    }

}


// ============================================================
// SAVE HISTORY
// ============================================================

function saveHistory(transaction) {

    const history = getHistory();

    history.unshift(transaction);

    const limitedHistory =
        history.slice(0, 50);

    localStorage.setItem(
        "payshield_history",
        JSON.stringify(limitedHistory)
    );

}


// ============================================================
// UPDATE DASHBOARD
// ============================================================

function updateStats() {

    const history = getHistory();

    const total = history.length;

    const fraud = history.filter(
        item => item.fraud === true
    ).length;

    const legitimate = total - fraud;

    const rate =
        total > 0
            ? ((fraud / total) * 100).toFixed(1)
            : "0";


    totalTransactionsElement.textContent =
        total;

    fraudCountElement.textContent =
        fraud;

    legitimateCountElement.textContent =
        legitimate;

    fraudRateElement.textContent =
        rate + "%";

}


// ============================================================
// DISPLAY HISTORY
// ============================================================

function loadHistory() {

    const history = getHistory();

    historyBody.innerHTML = "";


    if (history.length === 0) {

        historyBody.innerHTML = `
            <tr>
                <td colspan="5" class="empty">
                    No transactions analyzed yet.
                </td>
            </tr>
        `;

        updateStats();

        return;
    }


    history.forEach((item, index) => {

        const row = document.createElement("tr");


        let riskText = "";

        let riskClass = "";


        if (item.probability >= 0.75) {

            riskText = "🔴 CRITICAL";

            riskClass = "risk-high";

        }

        else if (item.probability >= 0.50) {

            riskText = "🔴 HIGH";

            riskClass = "risk-high";

        }

        else if (item.probability >= 0.20) {

            riskText = "🟡 MEDIUM";

            riskClass = "risk-low";

        }

        else {

            riskText = "🟢 LOW";

            riskClass = "risk-low";

        }


        const percentage =
            item.probability <= 1
                ? item.probability * 100
                : item.probability;


        row.innerHTML = `

            <td>
                ${index + 1}
            </td>

            <td>
                ${item.time}
            </td>

            <td>
                ₹${Number(item.amount).toFixed(2)}
            </td>

            <td class="${riskClass}">
                ${riskText}
            </td>

            <td>
                ${percentage.toFixed(2)}%
            </td>

        `;


        historyBody.appendChild(row);

    });


    updateStats();

}


// ============================================================
// ANALYZE TRANSACTION
// ============================================================

async function analyzeTransaction() {

    analyzeButton.disabled = true;

    loadingElement.style.display = "block";


    try {

        // ----------------------------------------------------
        // TIME
        // ----------------------------------------------------

        const time =
            Number(
                document.getElementById("time").value
            );


        if (!Number.isFinite(time)) {

            throw new Error(
                "Please enter a valid transaction time."
            );

        }


        // ----------------------------------------------------
        // AMOUNT
        // ----------------------------------------------------

        const amount =
            Number(
                document.getElementById("amount").value
            );


        if (!Number.isFinite(amount)) {

            throw new Error(
                "Please enter a valid transaction amount."
            );

        }


        if (amount < 0) {

            throw new Error(
                "Transaction amount cannot be negative."
            );

        }


        // ----------------------------------------------------
        // CREATE 30 FEATURES
        // ----------------------------------------------------

        const features = [];

        // Time
        features.push(time);


        // V1 - V28
        for (let i = 1; i <= 28; i++) {

            const value =
                Number(
                    document.getElementById(`V${i}`).value
                );


            if (!Number.isFinite(value)) {

                throw new Error(
                    `Please enter a valid value for V${i}.`
                );

            }


            features.push(value);

        }


        // Amount
        features.push(amount);


        // ----------------------------------------------------
        // CHECK 30 FEATURES
        // ----------------------------------------------------

        if (features.length !== 30) {

            throw new Error(
                `Expected 30 features but created ${features.length}.`
            );

        }


        // ----------------------------------------------------
        // SEND TO BACKEND
        // ----------------------------------------------------

        const response =
            await fetch(
                "http://127.0.0.1:8000/predict",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json",

                        "Accept":
                            "application/json"
                    },

                    body: JSON.stringify({
                        features: features
                    })
                }
            );


        // ----------------------------------------------------
        // READ RESPONSE
        // ----------------------------------------------------

        const data =
            await response.json();


        if (!response.ok) {

            let message =
                "Backend error.";

            if (data.detail) {

                if (Array.isArray(data.detail)) {

                    message =
                        data.detail
                            .map(item => item.msg)
                            .join(", ");

                }

                else {

                    message =
                        data.detail;

                }

            }

            else if (data.message) {

                message =
                    data.message;

            }


            throw new Error(message);

        }


        if (data.status !== "success") {

            throw new Error(
                data.message ||
                "Transaction analysis failed."
            );

        }


        // ----------------------------------------------------
        // GET RESULT
        // ----------------------------------------------------

        const probability =
            Number(
                data.fraud_probability
            );


        const result =
            data.result;


        const riskLevel =
            data.risk_level;


        const recommendation =
            data.recommendation;


        if (!Number.isFinite(probability)) {

            throw new Error(
                "Invalid fraud probability received."
            );

        }


        // ----------------------------------------------------
        // DISPLAY RESULT
        // ----------------------------------------------------

        displayResult(
            probability,
            result,
            riskLevel,
            recommendation
        );


        // ----------------------------------------------------
        // SAVE HISTORY
        // ----------------------------------------------------

        saveHistory({

            time: time,

            amount: amount,

            probability: probability,

            fraud: result === "Fraud",

            result: result,

            risk: riskLevel,

            timestamp:
                new Date().toISOString()

        });


        // ----------------------------------------------------
        // UPDATE HISTORY
        // ----------------------------------------------------

        loadHistory();

    }


    catch (error) {

        shieldElement.textContent = "❌";

        shieldElement.style.background =
            "rgba(239,68,68,0.10)";

        shieldElement.style.borderColor =
            "rgba(239,68,68,0.25)";


        resultTitleElement.textContent =
            "ANALYSIS FAILED";


        resultSubtitleElement.textContent =
            "Unable to process this transaction.";


        probabilityElement.textContent =
            "—";


        riskPillElement.textContent =
            "ERROR";


        riskPillElement.style.color =
            "#fca5a5";


        riskPillElement.style.background =
            "rgba(239,68,68,0.12)";


        recommendationElement.textContent =
            error.message ||
            "Unable to connect to PayShield AI backend.";

    }


    finally {

        analyzeButton.disabled = false;

        loadingElement.style.display = "none";

    }

}


// ============================================================
// DISPLAY RESULT
// ============================================================

function displayResult(
    probability,
    result,
    riskLevel,
    recommendation
) {

    const percentage =
        probability <= 1
            ? probability * 100
            : probability;


    probabilityElement.textContent =
        percentage.toFixed(2) + "%";


    // --------------------------------------------------------
    // FRAUD
    // --------------------------------------------------------

    if (result === "Fraud") {

        shieldElement.textContent =
            "🚨";

        shieldElement.style.background =
            "rgba(239,68,68,0.10)";

        shieldElement.style.borderColor =
            "rgba(239,68,68,0.25)";


        resultTitleElement.textContent =
            "TRANSACTION FLAGGED";


        resultSubtitleElement.textContent =
            "Potential fraudulent activity detected.";


        riskPillElement.textContent =
            riskLevel + " RISK";


        riskPillElement.style.color =
            "#fca5a5";

        riskPillElement.style.background =
            "rgba(239,68,68,0.12)";


        recommendationElement.textContent =
            "⚠️ Recommendation: " +
            recommendation;

    }


    // --------------------------------------------------------
    // LEGITIMATE
    // --------------------------------------------------------

    else {

        shieldElement.textContent =
            "🛡️";

        shieldElement.style.background =
            "rgba(34,197,94,0.10)";

        shieldElement.style.borderColor =
            "rgba(34,197,94,0.20)";


        resultTitleElement.textContent =
            "TRANSACTION VERIFIED";


        resultSubtitleElement.textContent =
            "No significant fraud indicators detected.";


        riskPillElement.textContent =
            riskLevel + " RISK";


        if (riskLevel === "MEDIUM") {

            riskPillElement.style.color =
                "#fde68a";

            riskPillElement.style.background =
                "rgba(234,179,8,0.12)";

        }

        else {

            riskPillElement.style.color =
                "#86efac";

            riskPillElement.style.background =
                "rgba(34,197,94,0.12)";

        }


        recommendationElement.textContent =
            "✅ Recommendation: " +
            recommendation;

    }

}


// ============================================================
// CLEAR HISTORY
// ============================================================

function clearHistory() {

    const history = getHistory();


    if (history.length === 0) {

        alert(
            "There are no transactions to clear."
        );

        return;

    }


    const confirmed =
        confirm(
            "Are you sure you want to clear all transaction history?"
        );


    if (!confirmed) {

        return;

    }


    localStorage.removeItem(
        "payshield_history"
    );


    loadHistory();

    resetResult();


    alert(
        "Transaction history cleared successfully."
    );

}


// ============================================================
// EXPORT REPORT
// ============================================================

function exportReport() {

    const history = getHistory();


    if (history.length === 0) {

        alert(
            "No transactions available to export."
        );

        return;

    }


    let csv =
        "No,Date,Time,Amount,Risk,Result,Fraud Probability\n";


    history.forEach((item, index) => {

        const probability =
            item.probability <= 1
                ? item.probability * 100
                : item.probability;


        let risk;


        if (item.probability >= 0.75) {

            risk = "CRITICAL";

        }

        else if (item.probability >= 0.50) {

            risk = "HIGH";

        }

        else if (item.probability >= 0.20) {

            risk = "MEDIUM";

        }

        else {

            risk = "LOW";

        }


        csv +=
            `${index + 1},` +
            `"${item.timestamp || ""}",` +
            `${item.time},` +
            `${item.amount},` +
            `${risk},` +
            `${item.result},` +
            `${probability.toFixed(2)}%\n`;

    });


    const blob =
        new Blob(
            [csv],
            {
                type:
                    "text/csv;charset=utf-8;"
            }
        );


    const url =
        URL.createObjectURL(blob);


    const link =
        document.createElement("a");


    link.href = url;

    link.download =
        "PayShield_AI_Transaction_Report.csv";


    document.body.appendChild(link);

    link.click();

    document.body.removeChild(link);


    URL.revokeObjectURL(url);

}


// ============================================================
// INITIALIZE
// ============================================================

loadHistory();


// ============================================================
// MAKE FUNCTIONS AVAILABLE TO HTML BUTTONS
// ============================================================

window.analyzeTransaction =
    analyzeTransaction;

window.loadLegitimate =
    loadLegitimate;

window.loadFraud =
    loadFraud;

window.clearHistory =
    clearHistory;

window.exportReport =
    exportReport;