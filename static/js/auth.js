async function refreshAccessToken() {

    const refresh = localStorage.getItem("refresh");

    const response = await fetch("/api/auth/token/refresh/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ refresh: refresh })
    });

    const data = await response.json();

    localStorage.setItem("access", data.access);

    return data.access;
}


async function apiRequest(url, options = {}) {

    let access = localStorage.getItem("access");

    options.headers = {
        ...options.headers,
        "Authorization": "Bearer " + access
    };

    let response = await fetch(url, options);

    if (response.status === 401) {

        access = await refreshAccessToken();

        options.headers["Authorization"] = "Bearer " + access;

        response = await fetch(url, options);
    }

    return response;
}