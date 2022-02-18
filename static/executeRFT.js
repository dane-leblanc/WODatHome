"use strict";

let minutes = 0;
let seconds = 0;
let tenths = 0;
let interval = 0;

const $appendMinutes = $("#minutes");
const $appendSeconds = $("#seconds");
const $appendTenths = $("#tenths");
const $startBtn = $("#button-start");
const $stopBtn = $("#button-stop");
const $logBtn = $("#button-log");

$startBtn.on("click", function () {
  clearInterval(interval);
  interval = setInterval(startTimer, 10);
});

$stopBtn.on("click", function () {
  clearInterval(interval);
});

$logBtn.on("click", function () {
  console.log("LOG");
  $("#log-container").removeClass("collapse");
});

function startTimer() {
  tenths++;

  if (tenths <= 9) {
    $appendTenths.html("0" + tenths);
  }

  if (tenths > 9) {
    $appendTenths.html(tenths);
  }

  if (tenths > 99) {
    seconds++;
    $appendSeconds.html("0" + seconds);
    tenths = 0;
    $appendTenths.html("0" + tenths);
  }

  if (seconds > 9) {
    $appendSeconds.html(seconds);
  }

  if (seconds > 59) {
    minutes++;
    $appendMinutes.html("0" + minutes);
    seconds = 0;
    $appendSeconds.html("0" + seconds);
  }

  if (minutes > 9) {
    $appendMinutes.html(minutes);
  }
}
