async function submit_link() {
  const link = document.querySelector("#link").value;

  try {
    const response = await fetch("/home/submit_link", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: localStorage.getItem("session_token"),
      },
      body: JSON.stringify({
        link: link,
      }),
    });

    const result = await response.json();
    console.log(result);
  } catch (err) {
    console.log("network error");
  }
}
