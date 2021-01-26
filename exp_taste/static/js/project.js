function selectLot(lot_id) {
    const selected = document.getElementById(lot_id);
    const other_id = lot_id === "lot_a" ? "lot_b" : "lot_a";
    console.log(lot_id);
    console.log(other_id);
    const other = document.getElementById(other_id);
    const selected_price = parseInt(selected.getAttribute("data-sale-usd"));
    const other_price = parseInt(other.getAttribute("data-sale-usd"));
    let prices = document.getElementsByClassName("price");
    for (p of prices) {
        p.classList.remove("hidden");
    }
    document.getElementById("answer").classList.remove("hidden");
    let result = document.getElementById("result");
    if (selected_price >= other_price) {
        console.log(selected_price);
        console.log(other_price);
        result.textContent = "Correct!"
        result.classList.add("text-success");
        selected.classList.add("correct")
    } else {
        result.textContent = "Incorrect!"
        selected.classList.add("incorrect")
        result.classList.add("text-danger");
    }
}