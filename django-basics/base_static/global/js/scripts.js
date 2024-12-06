function scope() {
    const forms = document.querySelectorAll(".form-delete")

    for (let f of forms) {
        f.addEventListener('submit', (e) => {
            e.preventDefault();

            const confirmed = window.confirm("Delete this recipe?")
            if (confirmed) {
                f.submit()
            }
        })
    }

}
scope()