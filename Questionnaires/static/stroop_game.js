document.addEventListener("DOMContentLoaded", () => {
  const color1 = document.getElementById("color1");
  const color2 = document.getElementById("color2");
  const yesButton = document.getElementById("yesButton");
  const noButton = document.getElementById("noButton");
  const pointsDiv = document.getElementById("points");
  const rgb2hex = (rgb) =>
    `#${rgb
      .match(/^rgb\((\d+),\s*(\d+),\s*(\d+)\)$/)
      .slice(1)
      .map((n) => parseInt(n, 10).toString(16).padStart(2, "0"))
      .join("")}`;
  let interval = 0;
  let timerRuns = false;
  let points = 0;
  const colors = [
    ["modrá", "#0000ff"],
    ["zelená", "#008000"],
    ["červená", "#ff0000"],
    ["žltá", "#ffff00"],
    ["ružová", "#ff69b4"],
  ];

  // function getKeyByValue(object, value) {
  //   return Object.keys(object).find((key) => object[key] === value);
  // }

  const colorObj = {
    "modrá": "#0000ff",
    "zelená": "#008000",
    "červená": "#ff0000",
    "žltá": "#ffff00",
    "ružová": "#ff69b4",
  };

  // console.log(colorObj["ružová"])
  // console.log(getKeyByValue(colorObj, "#FF69B4"))
  const timer = document.getElementById("timer");
  const seconds = 120;
  timer.innerText = "2:00";
  randomizeColors();

  let timeToGo = seconds;

  function randomizeColors() {
    const r1 = Math.floor(Math.random() * colors.length);
    const r2 = Math.floor(Math.random() * colors.length);
    const r3 = Math.floor(Math.random() * colors.length);
    const r4 = Math.floor(Math.random() * colors.length);

    color1.innerText = colors[r1][0];
    color2.innerText = colors[r2][0];
    color1.style.color = colors[r3][1];
    color2.style.color = colors[r4][1];
  }

  function tickTimer() {
    const minutes = Math.floor(timeToGo / 60);
    const seconds = timeToGo % 60;

    timer.innerText = `${minutes}:${seconds < 10 ? "0" : ""}${seconds}`;
    timeToGo--;
    if (timeToGo < 0) {
      clearInterval(interval);
      timer.innerText = "0:00";
      yesButton.style.visibility="hidden";
      noButton.style.visibility="hidden";
      alert("KONIEC")
    }
  }

  yesButton.addEventListener("click", yesNoFunction);
  yesButton.answer = "yes";
  noButton.addEventListener("click", yesNoFunction);
  noButton.answer = "no";

  function yesNoFunction(evt) {
    // console.log(evt.target.answer);
    if (!timerRuns) {
      interval = setInterval(tickTimer, 1000);
      timerRuns = true;
    }
    console.log(rgb2hex(color1.style.color), colorObj[color2.innerText]);
    //TODO a treba vygenerovat nove farby
    if (
      rgb2hex(color1.style.color) === colorObj[color2.innerText] &&
      evt.target.answer === "yes"
    ) {
      console.log("yay");
      points++;
      pointsDiv.innerText = points;
    } else if (
      rgb2hex(color1.style.color) !== colorObj[color2.innerText] &&
      evt.target.answer === "no"
    ) {
      console.log("yay");
      points++;
      pointsDiv.innerText = points;
    } else {
      console.log("nay");
      points--;
      pointsDiv.innerText = points;
    }
    randomizeColors();
  }
});
