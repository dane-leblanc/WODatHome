"use strict";

let seconds = 60;
let tenths = 0;
let interval = 0;

let excList = $("#excList li");
let workoutMinutes = excList.length;
let currMinute = 1;

const $appendSeconds = $("#seconds");
const $appendTenths = $("#tenths");
const $startBtn = $("#button-start");
const $stopBtn = $("#button-stop");
const $logBtn = $("#button-log");

const $minuteDisplay = $("#minuteDisplay");
const $appendCurrExc = $("#currentExc");
const $appendNextExc = $("#nextExc");

$startBtn.on("click", function () {
  $(`#excList li:nth-child(${currMinute})`).addClass("font-weight-bold");
  clearInterval(interval);
  interval = setInterval(startCountdown, 10);
});

$stopBtn.on("click", function () {
  clearInterval(interval);
});

$logBtn.on("click", function () {
  $("#log-container").removeClass("collapse");
});

function startCountdown() {
  tenths--;

  if (tenths > 9) {
    $appendTenths.html(tenths);
  }
  if (tenths < 0) {
    seconds--;
    $appendSeconds.html(seconds);
    tenths = 99;
    $appendTenths.html(tenths);
  }
  if (tenths <= 9) {
    $appendTenths.html("0" + tenths);
  }
  if (seconds <= 9) {
    $appendSeconds.html("0" + seconds);
  }
  if (seconds == 0) {
    nextMinute();
  }
}

function nextMinute() {
  currMinute++;
  $(`#excList li:nth-child(${currMinute})`).addClass("font-weight-bold");
  if (currMinute == workoutMinutes) {
    clearInterval(interval);
    return alert("Exercise Complete!");
  }
  seconds = 60;
  tenths = 0;
  $appendSeconds.html(seconds);
  $appendTenths.html("0" + tenths);
  displayExercises();
  clearInterval(interval);
  interval = setInterval(startCountdown, 10);
}

function displayExercises() {
  $minuteDisplay.text(currMinute + 1);
  $appendCurrExc.text(excList[currMinute].innerText);
  if (currMinute + 1 !== workoutMinutes) {
    $appendNextExc.text(excList[currMinute + 1].innerText);
  } else {
    $appendNextExc.text("Last one!!!");
  }
}

displayExercises();
