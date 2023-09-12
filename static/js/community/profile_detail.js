window.onload = () => {
    const csrftoken = document.getElementsByName("csrfmiddlewaretoken")[0].value
    const threadId = document.getElementsByName("thread_id")[0].value;
    document.getElementById("js_add_comment").addEventListener("click", () => {
        const newThreadEl = document.getElementsByName("new_comment")[0];
        fetch("/social/api/comments", {
            method: "POST",
            headers: {
                "X-CSRFToken": csrftoken,
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                "thread": threadId,
                "body": newThreadEl.value,
            }),
        }).then((response) => {
            if (!response.ok) {
                let err = new Error("HTTP status code: " + response.status)
                err.response = response;
                err.status = response.status;
                throw err;
            }
            return response;
        }).then(
            () => {
                alert("소식을 남겼어요.");
                location.reload();
            }
        )
    });

    document.getElementById("js_modify_thread").addEventListener("click", () => {
        const threadEl = document.getElementsByName("thread")[0];
        fetch(`/social/api/threads/${threadId}`, {
            method: "PATCH",
            headers: {
                "X-CSRFToken": csrftoken,
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                "body": threadEl.value,
            }),
        }).then((response) => {
            if (!response.ok) {
                let err = new Error("HTTP status code: " + response.status)
                err.response = response;
                err.status = response.status;
                throw err;
            }
            return response;
        }).then(
            () => {
                alert("소개를 수정했습니다.");
                location.reload();
            }
        )
    });
}
