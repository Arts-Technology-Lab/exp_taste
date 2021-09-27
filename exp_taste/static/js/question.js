window.addEventListener('load', () => {
    const qtype = document.getElementById("id_qtype").value
    document
        .getElementById("multichoiceoption_set-group")
        .hidden = (qtype !== '2');

    document
        .getElementById("id_qtype")
        .addEventListener('change', (e) => {
            document
                .getElementById("multichoiceoption_set-group")
                .hidden = (e.target.value !== '2');
        });
})
