"use strict";

let minutes = 0;
let seconds = 0;
let tenths = 0;
let interval = 0;
let exercises = [];
let workout = {};

const $workoutId = $("#workout").attr("data-id");
const $appendMinutes = $("#minutes");
const $appendSeconds = $("#seconds");
const $appendTenths = $("#tenths");
const $startBtn = $("#button-start");
const $display = $("#display")
const $logBtn = $("#button-log");

getExercises();
getWorkout();

$logBtn.on("click", function () {
  $("#log-container").removeClass("collapse");
});

$startBtn.on("click", function () {
  minutes = workout.stage_time;
  clearInterval(interval);
  interval = setInterval(startCountdown, 10);
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
  if (seconds < 0) {
    minutes--;
    $appendMinutes.html("0" + minutes);
    seconds = 59;
    $appendSeconds.html(seconds);
  }
  if ((minutes = 0)) {
    clearInterval(interval);
    alert("next stage");
  }
}

async function getExercises() {
    const res = await axios.get(`/api/workout_exercises/${$workoutId}`);
    exercises = res.data;
  }
  
  async function getWorkout() {
    const res = await axios.get(`/api/workout/${$workoutId}`);
    workout = res.data;
  }