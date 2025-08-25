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
    let q = result.message;

    let topics = [];
    let topicS = ``;
    for (let i = 0; i < q.topicTags.length; i++) {
      topicS += `<span class="topic-tag">${q.topicTags[i]["name"]}</span>`;
    }

    let temp = ``;
    temp += `
    <div class="question-card">
        <!-- Line 1: Question number + title -->
        <div class="question-title">${q.questionId}. ${q.title}</div>

        <!-- Line 2: Difficulty -->
        <div class="difficulty ${q.difficulty}">${q.difficulty}</div>

        <!-- Line 3: Topics -->
        <div class="topics">
          ${topicS}
        </div>

        <!-- Line 4: Status -->
        <div class="status">${result.stat}</div>
      </div>
    
    `;
    temp += `
    ${document.querySelector(".question-container").innerHTML}
    `;
    document.querySelector(".question-container").innerHTML = temp;
  } catch (err) {
    console.log("network error");
  }
}

async function get_link() {
  try {
    const response = await fetch("/home/get_link", {
      method: "GET",
      headers: { Authorization: localStorage.getItem("session_token") },
    });

    const result = await response.json();
    let ques = result.message;
    if (ques.length == 0) {
      alert("no questions in backlog");
      return;
    }
    let temp = ``;
    for (let i = 0; i < ques.length; i++) {
      let q = ques[i];

      let topics = [];
      let topicS = ``;
      for (let i = 0; i < q.tags.length; i++) {
        topicS += `<span class="topic-tag">${q.tags[i]}</span>`;
      }

      temp += `
      <br>
      <div class="question-card">
  <a href="${q.url}" target="_blank" style="text-decoration: none; color: inherit;">
    
      <div class="question-title">${q.number}. ${q.title}</div>
      <div class="difficulty ${q.difficulty}">${q.difficulty}</div>
      <div class="topics">${topicS}</div>
    
  </a>
  <button onclick="mark_compelete(${q.number})" class="butt">Mark Compeleted</button>
  </div>
`;
    }

    document.querySelector(".Gquestion-container").innerHTML = temp;
  } catch (err) {
    console.log("network error");
  }
}

async function mark_compelete(number) {
  try {
    const response = await fetch("/home/mark_compelete", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: localStorage.getItem("session_token"),
      },
      body: JSON.stringify({
        number: number,
      }),
    });

    const result = await response.json();
    console.log(result);

    if (result.message == "success") {
      document.querySelector(".Gquestion-container").innerHTML = ``;
    }
  } catch (err) {
    alert("network error");
  }
}
