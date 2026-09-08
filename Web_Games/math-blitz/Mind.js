let score = 0;
let level = 1;
let time = 10;
let combo = 0;

let currentAnswer;
let timer;

let highscore = localStorage.getItem("highscore") || 0;
document.getElementById("highscore").innerText = highscore;

function getSettings() {
  let mode = document.getElementById("mode").value;

  if (mode === "easy") return { max: 10, time: 10 };
  if (mode === "medium") return { max: 20, time: 7 };
  if (mode === "hard") return { max: 50, time: 5 };
}

function generateQuestion() {
  let settings = getSettings();

  let a = Math.floor(Math.random() * settings.max);
  let b = Math.floor(Math.random() * settings.max);

  let ops = ["+", "-", "*"];
  let op = ops[Math.floor(Math.random() * ops.length)];

  let question = `${a} ${op} ${b}`;
  currentAnswer = eval(question);

  document.getElementById("question").innerText = question;
}

function startTimer() {
  clearInterval(timer);

  let settings = getSettings();
  time = settings.time;

  document.getElementById("time").innerText = time;

  timer = setInterval(() => {
    time--;
    document.getElementById("time").innerText = time;

    if (time <= 0) {
      clearInterval(timer);
      document.getElementById("feedback").innerText = "⏰ Time's up!";
      playSound("wrong");
      nextRound(false);
    }
  }, 1000);
}

function playSound(type) {
  if (type === "correct") {
    document.getElementById("correctSound").play();
  } else {
    document.getElementById("wrongSound").play();
  }
}

function submitAnswer() {
  let userAnswer = parseInt(document.getElementById("answer").value);

  if (userAnswer === currentAnswer) {
    combo++;
    let bonus = combo >= 3 ? 5 : 0;

    score += 10 + bonus;

    document.getElementById("feedback").innerText =
      `✅ Correct! ${bonus ? "+ Combo Bonus 🔥" : ""}`;

    playSound("correct");
    nextRound(true);
  } else {
    combo = 0;
    score = Math.max(0, score - 5);

    document.getElementById("feedback").innerText = "❌ Wrong!";
    playSound("wrong");
    nextRound(false);
  }
}

function nextRound(correct) {
  clearInterval(timer);

  if (correct) level++;

  document.getElementById("score").innerText = score;
  document.getElementById("level").innerText = level;
  document.getElementById("combo").innerText = combo;

  // High Score Save
  if (score > highscore) {
    highscore = score;
    localStorage.setItem("highscore", highscore);
    document.getElementById("highscore").innerText = highscore;
  }

  document.getElementById("answer").value = "";

  generateQuestion();
  startTimer();
}

// Start Game
generateQuestion();
startTimer();