"use strict";

let minutes = 0;
let seconds = 0;
let tenths = 0;
let interval = 0;
let exercises = [];
let workout = {};
let restTime = 0;
let workoutStages = [];
let currStage = 1;
let rest = false;

const $workoutId = $("#workout").attr("data-id");
const $appendMinutes = $("#minutes");
const $appendSeconds = $("#seconds");
const $appendTenths = $("#tenths");
const $startBtn = $("#button-start");
const $stopBtn = $("#button-stop");
const $display = $("#display");
const $logBtn = $("#button-log");

getExercises();
getWorkout();

$logBtn.on("click", function () {
  $("#log-container").removeClass("collapse");
});

$startBtn.on("click", function () {
  minutes = workout.stage_time;
  splitIntoStages();
  displayStageWorkouts(currStage);
  clearInterval(interval);
  interval = setInterval(startCountdown, 10);
});

$stopBtn.on("click", function () {
  clearInterval(interval);
});

function displayStageWorkouts(stage) {
  let $displayDiv = $("<div>");
  let $stageP = $(`<p><u>Stage ${currStage}</u></p>`);
  $stageP.appendTo($displayDiv);
  for (let exercise of workoutStages[stage - 1]) {
    let $newP = $("<p>");
    $newP.text(`${exercise.count} ${exercise.count_type} of ${exercise.name}`);
    $newP.appendTo($displayDiv);
  }
  $display.html($displayDiv);
}

function displayRest() {
  let $displayDiv = $("<div>");
  let $restH2 = $("<h2>REST</h2>");
  $restH2.appendTo($displayDiv);
  $display.html($displayDiv);
}

function splitIntoStages() {
  let exercisesPerStage =
    (exercises.length - workout.stages + 1) / workout.stages;
  let tick = 0;
  while (tick < exercises.length) {
    workoutStages.push(exercises.slice(tick, tick + exercisesPerStage));
    tick = tick + exercisesPerStage + 1;
  }
  restTime = exercises[exercisesPerStage].count;
}

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
    seconds = 59;
    $appendSeconds.html(seconds);
    minutes--;
    $appendMinutes.html("0" + minutes);
  }
  if (minutes === 0 && seconds === 0 && tenths === 0) {
    clearInterval(interval);
    nextStage();
  }
}

function nextStage() {
  if (currStage === workoutStages.length) {
    let $displayDiv = $("<div>");
    let $doneH2 = $(
      "<h2>Workout Complete! (Don't forget to log your results)</h2>"
    );
    $doneH2.appendTo($displayDiv);
    $display.html($displayDiv);
    return;
  }
  if (rest === false) {
    rest = true;
    displayRest();
    let restMins = Math.floor(restTime / 60);
    let restSecs = Math.floor(restTime % 60);
    minutes = restMins;
    seconds = restSecs;
    interval = setInterval(startCountdown, 10);
  } else {
    rest = false;
    currStage++;
    displayStageWorkouts(currStage);
    minutes = workout.stage_time;
    interval = setInterval(startCountdown, 10);
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
