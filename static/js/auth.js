// Register a User

async function register() {
  const user_email = document.querySelector("#r_user").value;
  const user_password = document.querySelector("#r_pass").value;

  try {
    const response = await fetch("/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user_email: user_email,
        user_password: user_password,
      }),
    });

    const result = await response.json();
    if (!response.ok) {
      alert(result.error || "error");
      return;
    }

    if (result.message == "success") {
      localStorage.setItem("session_token", result.token);
      window.location.href = "/home";
    } else {
      alert(result.error || "error");
    }
  } catch (err) {
    alert("network error");
  }
}

// Login User

async function login() {
  const user_email = document.querySelector("#l_user").value;
  const user_password = document.querySelector("#l_pass").value;

  try {
    const response = await fetch("/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user_email: user_email,
        user_password: user_password,
      }),
    });
    if (!response.ok) {
      console.log("Server error");
      return;
    }

    const result = await response.json();

    if (result.message == "success") {
      localStorage.setItem("session_token", result.token);
      window.location.href = "/home";
    } else {
      alert(result.error || "error");
    }
  } catch (err) {
    alert("network error");
  }
}
