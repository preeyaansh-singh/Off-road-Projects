const choices = ["rock", "paper", "scissors"];
const symbols = { rock: "◆", paper: "▤", scissors: "✂" };
const beats = { rock: "scissors", paper: "rock", scissors: "paper" };
const labels = { rock: "ROCK", paper: "PAPER", scissors: "SCISSORS" };

const elements = {
  card: document.querySelector(".match-card"),
  matchStatus: document.querySelector(".round-kicker"),
  round: document.querySelector("#round-number"),
  playerScore: document.querySelector("#player-score"),
  cpuScore: document.querySelector("#cpu-score"),
  playerMove: document.querySelector("#player-move"),
  cpuMove: document.querySelector("#cpu-move"),
  playerCaption: document.querySelector("#player-caption"),
  cpuCaption: document.querySelector("#cpu-caption"),
  result: document.querySelector("#result-chip"),
  prompt: document.querySelector("#game-prompt"),
  streak: document.querySelector("#streak-value"),
  rounds: document.querySelector("#rounds-played"),
  announcement: document.querySelector("#announcement"),
  choices: [...document.querySelectorAll(".choice-button")],
};

const state = {
  playerScore: 0,
  cpuScore: 0,
  rounds: 0,
  streak: 0,
  matchOver: false,
};

function computerChoice() {
  return choices[Math.floor(Math.random() * choices.length)];
}

function setMove(element, choice) {
  element.innerHTML = `<span class="move-symbol">${symbols[choice]}</span>`;
  element.classList.remove("has-move", "is-winner", "is-loser");
  void element.offsetWidth;
  element.classList.add("has-move");
}

function updateScoreboard() {
  elements.playerScore.textContent = state.playerScore;
  elements.cpuScore.textContent = state.cpuScore;
  elements.rounds.textContent = state.rounds;
  elements.streak.textContent = state.streak;
  elements.round.textContent = `ROUND ${String(state.rounds + 1).padStart(2, "0")}`;
}

function finishMatch(winner) {
  state.matchOver = true;
  elements.matchStatus.textContent = "MATCH COMPLETE";
  elements.card.classList.remove("match-win", "match-loss");
  elements.card.classList.add(winner === "player" ? "match-win" : "match-loss");
  elements.result.className = `result-chip ${winner === "player" ? "win" : "loss"}`;
  elements.result.textContent = winner === "player" ? "MATCH WON" : "MATCH LOST";
  elements.prompt.textContent = winner === "player" ? "You own the arena." : "The CPU takes this one.";
  elements.choices.forEach((button) => { button.disabled = true; });
  elements.announcement.textContent = winner === "player"
    ? "Match won! You beat the CPU."
    : "Match lost. The CPU wins.";
}

function playRound(playerChoice) {
  if (state.matchOver) return;

  const cpu = computerChoice();
  state.rounds += 1;
  setMove(elements.playerMove, playerChoice);
  setMove(elements.cpuMove, cpu);
  elements.playerCaption.textContent = labels[playerChoice];
  elements.cpuCaption.textContent = labels[cpu];
  elements.card.classList.remove("match-win", "match-loss", "match-draw");
  elements.result.className = "result-chip";

  let outcome;
  if (playerChoice === cpu) {
    outcome = "draw";
    state.streak = 0;
    elements.result.textContent = "IT'S A DRAW";
    elements.prompt.textContent = "Evenly matched. Go again.";
    elements.card.classList.add("match-draw");
  } else if (beats[playerChoice] === cpu) {
    outcome = "win";
    state.playerScore += 1;
    state.streak += 1;
    elements.playerMove.classList.add("is-winner");
    elements.cpuMove.classList.add("is-loser");
    elements.result.classList.add("win");
    elements.result.textContent = "YOU TAKE THE ROUND";
    elements.prompt.textContent = "Nice read. Keep it going.";
  } else {
    outcome = "loss";
    state.cpuScore += 1;
    state.streak = 0;
    elements.cpuMove.classList.add("is-winner");
    elements.playerMove.classList.add("is-loser");
    elements.result.classList.add("loss");
    elements.result.textContent = "CPU TAKES THE ROUND";
    elements.prompt.textContent = "Shake it off. Next round.";
  }

  updateScoreboard();
  elements.round.textContent = `ROUND ${String(state.rounds).padStart(2, "0")}`;
  elements.announcement.textContent = outcome === "draw"
    ? `Draw. You both chose ${playerChoice}.`
    : `You chose ${playerChoice}, CPU chose ${cpu}. You ${outcome === "win" ? "won" : "lost"} the round.`;

  if (state.playerScore === 3) finishMatch("player");
  if (state.cpuScore === 3) finishMatch("cpu");
}

function resetMatch() {
  state.playerScore = 0;
  state.cpuScore = 0;
  state.rounds = 0;
  state.streak = 0;
  state.matchOver = false;
  elements.matchStatus.textContent = "MATCH IN PROGRESS";
  elements.card.classList.remove("match-win", "match-loss", "match-draw");
  [elements.playerMove, elements.cpuMove].forEach((move) => {
    move.innerHTML = '<span class="move-symbol">?</span>';
    move.classList.remove("has-move", "is-winner", "is-loser");
  });
  elements.playerCaption.textContent = "YOUR MOVE";
  elements.cpuCaption.textContent = "WAITING...";
  elements.result.className = "result-chip";
  elements.result.textContent = "PICK YOUR MOVE";
  elements.prompt.textContent = "Choose your weapon";
  elements.choices.forEach((button) => { button.disabled = false; });
  elements.announcement.textContent = "New match started. Choose your move.";
  updateScoreboard();
}

elements.choices.forEach((button) => {
  button.addEventListener("click", () => playRound(button.dataset.choice));
});

document.querySelector("#reset-button").addEventListener("click", resetMatch);

document.addEventListener("keydown", (event) => {
  if (event.altKey || event.ctrlKey || event.metaKey || event.repeat) return;
  const keyChoices = { r: "rock", p: "paper", s: "scissors" };
  const choice = keyChoices[event.key.toLowerCase()];
  if (choice && !state.matchOver) playRound(choice);
});

updateScoreboard();
