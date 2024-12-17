(async function () {
    console.clear()
    const headers = {
        'Content-Type': 'application/json',
    }
    const body = JSON.stringify({
        username: "admin",
        password: "admin"
    })


    const init = {
        method: "POST",
        headers: headers,
        body: body
    }
    const response = await fetch("http://127.0.0.1:8000/api/token/", init)
    if (!response.ok) {
        console.log("Erro ao buscar dados", response.status)
        return
    }
    const json = await response.json()
    const AccesToken = json.access

    const headers2 = {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${AccesToken}`
    }
    const body2 = JSON.stringify({
        username: "admin",
        password: "admin"
    })


    const init2 = {
        method: "GET",
        headers: headers2,
    }
    const response2 = await fetch("http://127.0.0.1:8000/auth/api/me", init2)
    const me = await response2.json()
    console.log(me)


})()