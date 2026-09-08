let balance = 500;

function playGame() {
  let bet = parseInt(document.getElementById("bet").value);
  let guess = parseInt(document.getElementById("guess").value);
  let maxRange = parseInt(document.getElementById("difficulty").value);

  let result = document.getElementById("result");
  let poolDiv = document.getElementById("pool");

  if (bet > balance || bet <= 0) {
    result.innerHTML = "❌ Invalid Bet";
    return;
  }

  if (guess < 1 || guess > maxRange) {
    result.innerHTML = "❌ Guess out of range";
    return;
  }

  // Generate 10 numbers
  let pool = [];
  while (pool.length < 10) {
    let num = Math.floor(Math.random() * maxRange) + 1;
    if (!pool.includes(num)) pool.push(num);
  }

  // Show pool UI
  poolDiv.innerHTML = "";
  pool.forEach(num => {
    let ball = document.createElement("div");
    ball.classList.add("ball");
    ball.innerText = num;
    poolDiv.appendChild(ball);
  });

  let multiplier = maxRange == 50 ? 1.5 : maxRange == 100 ? 2 : 3;

  if (pool.includes(guess)) {
    let win = Math.floor(bet * multiplier);
    balance += win;
    result.innerHTML = `🎉 JACKPOT! You won ₹${win}`;
  } else {
    balance -= bet;
    result.innerHTML = `😢 You lost ₹${bet}`;
  }

  document.getElementById("balance").innerText = balance;

  if (balance <= 0) {
    result.innerHTML += "<br>💀 Game Over";
  }
}