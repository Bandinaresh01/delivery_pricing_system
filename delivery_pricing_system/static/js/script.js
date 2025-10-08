document.getElementById("priceForm").addEventListener("submit", async function(event) {
    event.preventDefault();

    const form = event.target;
    const data = {
        material_type: form.material_type.value,
        urgency: form.urgency.value,
        weight: parseFloat(form.weight.value),
        location_type: form.location_type.value,
        origin: form.origin.value,
        destination: form.destination.value
    };

    const resultDiv = document.getElementById("result");
    const errorDiv = document.getElementById("error");
    const priceP = document.getElementById("price");
    const ticketP = document.getElementById("ticket");
    const logsDiv = document.getElementById("logs");

    resultDiv.classList.add("hidden");
    errorDiv.classList.add("hidden");
    priceP.textContent = "";
    ticketP.textContent = "";
    logsDiv.textContent = "";

    try {
        const response = await fetch("/calculate_price", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || "Failed to calculate price");
        }

        const result = await response.json();

        priceP.textContent = `Total Price: $${result.total_price.toFixed(2)}`;
        ticketP.textContent = `Ticket ID: ${result.ticket_id}`;
        logsDiv.innerHTML = "<strong>Action Log:</strong><br>" + result.action_log.map(log => log + "<br>").join("");
        resultDiv.classList.remove("hidden");
    } catch (error) {
        errorDiv.textContent = error.message;
        errorDiv.classList.remove("hidden");
    }
});
