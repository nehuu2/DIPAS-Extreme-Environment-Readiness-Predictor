const form = document.getElementById("readinessForm");

const resultCard = document.getElementById("result");
const errorBox = document.getElementById("error");

const scoreElement = document.getElementById("score");
const scoreCopyElement = document.getElementById("score-copy");
const riskElement = document.getElementById("risk");

const recommendationsElement =
    document.getElementById("recommendations");


// ========================================
// SHOW ERROR
// ========================================

function showErrors(errors) {

    errorBox.innerHTML = "";

    errors.forEach(function (errorMessage) {

        const errorLine = document.createElement("div");

        errorLine.className = "validation-error";

        errorLine.textContent = errorMessage;

        errorBox.appendChild(errorLine);
    });

    errorBox.style.display = "block";

    resultCard.style.display = "none";

    errorBox.scrollIntoView({
        behavior: "smooth",
        block: "center"
    });
}


// ========================================
// HIDE ERROR
// ========================================

function hideError() {

    errorBox.innerHTML = "";

    errorBox.style.display = "none";
}


// ========================================
// VALIDATE ALL INPUTS
// ========================================

function validateInputs(data) {

    const errors = [];


    // Age
    if (data.age < 18 || data.age > 120) {

        errors.push(
            "Invalid Age: Please enter an age between 18 and 120."
        );
    }


    // Altitude
    if (data.altitude < 0) {

        errors.push(
            "Invalid Altitude: Please enter an altitude of 0 m or above."
        );
    }


    // Temperature
    if (
        data.temperature < -50 ||
        data.temperature > 60
    ) {

        errors.push(
            "Invalid Temperature: Please enter a temperature between -50°C and 60°C."
        );
    }


    // Humidity
    if (
        data.humidity < 0 ||
        data.humidity > 100
    ) {

        errors.push(
            "Invalid Humidity: Please enter humidity between 0% and 100%."
        );
    }


    // Sleep
    if (
        data.sleep_hours < 0 ||
        data.sleep_hours > 24
    ) {

        errors.push(
            "Invalid Sleep Hours: Please enter sleep hours between 0 and 24."
        );
    }


    // Resting Heart Rate
    if (data.resting_heart_rate <= 0) {

        errors.push(
            "Invalid Resting Heart Rate: Please enter a value greater than 0."
        );
    }


    // Hydration
    if (
        data.hydration_level < 0 ||
        data.hydration_level > 100
    ) {

        errors.push(
            "Invalid Hydration Level: Please enter hydration between 0% and 100%."
        );
    }


    return errors;
}


// ========================================
// FORM SUBMISSION
// ========================================

form.addEventListener("submit", async function (event) {

    event.preventDefault();

    hideError();

    resultCard.style.display = "none";


    // ========================================
    // GET INPUT VALUES
    // ========================================

    const data = {

        age: Number(
            document.getElementById("age").value
        ),

        altitude: Number(
            document.getElementById("altitude").value
        ),

        temperature: Number(
            document.getElementById("temperature").value
        ),

        humidity: Number(
            document.getElementById("humidity").value
        ),

        sleep_hours: Number(
            document.getElementById("sleep_hours").value
        ),

        resting_heart_rate: Number(
            document.getElementById("resting_heart_rate").value
        ),

        hydration_level: Number(
            document.getElementById("hydration_level").value
        )
    };


    // ========================================
    // FRONTEND VALIDATION
    // ========================================

    const validationErrors =
        validateInputs(data);


    if (validationErrors.length > 0) {

        showErrors(validationErrors);

        return;
    }


    // ========================================
    // SEND DATA TO BACKEND
    // ========================================

    try {

        const response = await fetch(
            "/readiness",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(data)
            }
        );


        const result =
            await response.json();


        // ========================================
        // BACKEND ERROR
        // ========================================

        if (!response.ok) {

            if (
                result.details &&
                Array.isArray(result.details)
            ) {

                const backendErrors =
                    result.details.map(function (error) {

                        const field =
                            error.loc &&
                            error.loc.length > 0
                                ? error.loc[error.loc.length - 1]
                                : "input";


                        return formatBackendValidationMessage(
                            field,
                            error.msg
                        );
                    });


                showErrors(backendErrors);

            } else {

                showErrors([
                    result.error ||
                    "Unable to process your assessment."
                ]);
            }

            return;
        }


        // ========================================
        // RESULT
        // ========================================

        const score =
            Number(result.readiness_score);

        const risk =
            result.risk_level;


        scoreElement.textContent =
            score.toFixed(2);


        if (scoreCopyElement) {

            scoreCopyElement.textContent =
                score.toFixed(2);
        }


        riskElement.textContent =
            risk;


        // ========================================
        // RISK COLOR
        // ========================================

        if (risk === "Low") {

            riskElement.style.color = "#17a675";

        } else if (risk === "Moderate") {

            riskElement.style.color = "#d88900";

        } else {

            riskElement.style.color = "#dc3f3f";
        }


        // ========================================
        // SCORE CIRCLE
        // ========================================

        const scoreCircle =
            document.querySelector(".score-circle");


        if (scoreCircle) {

            const safeScore =
                Math.max(
                    0,
                    Math.min(score, 100)
                );

            const degree =
                safeScore * 3.6;


            let circleColor =
                "#22b983";


            if (risk === "Moderate") {

                circleColor =
                    "#e0a11a";

            } else if (risk === "High") {

                circleColor =
                    "#dc3f3f";
            }


            scoreCircle.style.background =
                `conic-gradient(
                    ${circleColor} 0deg,
                    ${circleColor} ${degree}deg,
                    #d9e9ed ${degree}deg,
                    #d9e9ed 360deg
                )`;
        }


        // ========================================
        // RISK PANEL
        // ========================================

        const riskPanel =
            document.querySelector(".risk-panel");


        if (riskPanel) {

            if (risk === "Low") {

                riskPanel.style.background =
                    "#ecfbf5";

                riskPanel.style.borderColor =
                    "#ccefe1";

            } else if (risk === "Moderate") {

                riskPanel.style.background =
                    "#fff8e8";

                riskPanel.style.borderColor =
                    "#f5dfaa";

            } else {

                riskPanel.style.background =
                    "#fff0f0";

                riskPanel.style.borderColor =
                    "#f4cccc";
            }
        }


        // ========================================
        // RECOMMENDATIONS
        // ========================================

        recommendationsElement.innerHTML = "";


        if (
            Array.isArray(result.recommendations) &&
            result.recommendations.length > 0
        ) {

            result.recommendations.forEach(
                function (recommendation) {

                    const listItem =
                        document.createElement("li");

                    listItem.textContent =
                        recommendation;

                    recommendationsElement.appendChild(
                        listItem
                    );
                }
            );

        } else {

            const listItem =
                document.createElement("li");

            listItem.textContent =
                "No specific recommendations at this time.";

            recommendationsElement.appendChild(
                listItem
            );
        }


        // ========================================
        // SHOW RESULT
        // ========================================

        resultCard.style.display =
            "block";


        resultCard.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });

    }


    catch (error) {

        console.error(
            "DIPAS Backend Error:",
            error
        );


        showErrors([
            "Unable to connect to the DIPAS backend. Please make sure the Flask server is running."
        ]);
    }

});


// ========================================
// BACKEND VALIDATION MESSAGE
// ========================================

function formatBackendValidationMessage(
    field,
    message
) {

    if (field === "age") {

        return (
            "Invalid Age: Please enter an age between 18 and 120."
        );
    }


    if (field === "altitude") {

        return (
            "Invalid Altitude: Please enter an altitude of 0 m or above."
        );
    }


    if (field === "temperature") {

        return (
            "Invalid Temperature: Please enter a temperature between -50°C and 60°C."
        );
    }


    if (field === "humidity") {

        return (
            "Invalid Humidity: Please enter humidity between 0% and 100%."
        );
    }


    if (field === "sleep_hours") {

        return (
            "Invalid Sleep Hours: Please enter sleep hours between 0 and 24."
        );
    }


    if (field === "resting_heart_rate") {

        return (
            "Invalid Resting Heart Rate: Please enter a value greater than 0."
        );
    }


    if (field === "hydration_level") {

        return (
            "Invalid Hydration Level: Please enter hydration between 0% and 100%."
        );
    }


    return "Invalid Input: " + message;
}