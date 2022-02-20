"use strict";
const $excOptions = $("#exc-options");
const BASE_URL = "http://127.0.0.1:5000";
const $selectedList = $("#selected-exercises");
const $clearBtn = $("#clear-button");
let excList = [];

let excType = "";

if (typeof $stagesVal !== "undefined") {
  excType = "AMRAP";
} else if (typeof $rounds !== "undefined") {
  excType = "RFT";
} else if (typeof $workoutLength !== "undefined") {
  excType = "EMOM";
}

if (localStorage.time) {
  $("#time").val(+localStorage.time);
  $workoutLength = +localStorage.time;
}

if (localStorage.rounds) {
  $("#rounds").val(+localStorage.rounds);
  $rounds = +localStorage.rounds;
}

if (localStorage.restTime) {
  $("#rest-time").val(localStorage.restTime);
  $restTime = +localStorage.restTime;
}

if (localStorage.stageTime) {
  $("#stage-time").val(localStorage.stageTime);
  $stageTime = +localStorage.stageTime;
}

if (localStorage.excPerStage) {
  $("#exc-per-stage").val(localStorage.excPerStage);
  $excPerStageVal = +localStorage.excPerStage;
}

if (localStorage.stages) {
  $("#stages").val(localStorage.stages);
  $stagesVal = +localStorage.stages;
  setStages();
} else {
  setStages();
}

if (localStorage.excList) {
  for (let ex of JSON.parse(localStorage.excList)) {
    excList.push(ex);
  }
  if (excType === "AMRAP") {
    fillStages();
  } else {
    fillExercises();
  }
}

$clearBtn.on("click", function () {
  localStorage.clear();
  location.reload();
});

$("nav").on("click", "a", function () {
  localStorage.clear();
});

$excOptions.on("click", ".btn-success", function (e) {
  if (excType === "EMOM" && excList.length >= $workoutLength) {
    return alert("You don't have the time for another exercise");
  }
  if (excType === "AMRAP" && $stagesVal * $excPerStageVal == excList.length) {
    return alert("You cannot add another exercise");
  }
  let exerciseId = +$(e.target).attr("data-id");
  let exerciseName = $(e.target).attr("data-name");
  let newExc = {
    id: exerciseId,
    name: exerciseName,
  };
  excList.push(newExc);
  localStorage.setItem("excList", JSON.stringify(excList));
  if (excType === "AMRAP") {
    let index = excList.length - 1;
    appendExercise(newExc, index);
  } else {
    appendExercise(newExc);
  }
});

$selectedList.on("dblclick", ".li-exercise", function (e) {
  let excId = +$(e.target).attr("data-id");
  for (let ex of excList) {
    if (ex.id === excId) {
      let index = excList.indexOf(ex);
      excList.splice(index, 1);
      localStorage.setItem("excList", JSON.stringify(excList));
      $(e.target).remove();
      location.reload();
      return;
    }
  }
});

function fillExercises() {
  for (let exc of excList) {
    appendExercise(exc);
  }
}

function setStages() {
  let $stages = $("#stages").val();
  for (let i = 1; i <= +$stages; i++) {
    $(`<li>`).text(`Stage ${i}`).appendTo($selectedList);
    $(`<ul>`).attr("class", `stage-${i}`).appendTo($selectedList);
  }
}

function fillStages() {
  let index = 0;
  for (let exc of excList) {
    appendExercise(exc, index);
    index = index + 1;
  }
}

function appendExercise(exc, index) {
  let $newLi = $(
    `<li class = "li-exercise form-inline" data-id = ${exc.id}> ${exc.name}</li>`
  );
  if (excType === "AMRAP") {
    let currStage = Math.floor(index / $excPerStageVal) + 1;
    $newLi.appendTo(`.stage-${currStage}`);
  } else {
    $newLi.appendTo($selectedList);
  }
  let $count = $(
    `<input type="number" class="exc-list-count form-control-sm m-1" data-exc="${exc.id}" value="10"/>`
  );
  $count.appendTo($newLi);
  let $countType = $(
    `<select class="exc-list-select form-control-sm" data-exc="${exc.id}">
      <option value="reps">reps</option>
      <option value="seconds">seconds</option>
    </select>`
  );
  $countType.appendTo($newLi);
}

async function postWorkout(stages, stage_time) {
  let type = excType;
  let name = $("#workout-name").text();
  let username = $("#workout-name").attr("data-user");

  const WorkoutRes = await axios({
    url: `${BASE_URL}/api/workouts`,
    method: "POST",
    data: {
      username,
      type,
      name,
      stages,
      stage_time,
    },
  });
}

async function postWorkoutExercises(order, exercise_id) {
  let name = $("#workout-name").text();
  let count = $(`input[data-exc=${exercise_id}]`).val();
  let count_type = $(`select[data-exc=${exercise_id}]`).val();
  if (exercise_id === 500) {
    count = $("#rest-time").val();
    count_type = "seconds";
  }
  const WorkoutExcRes = await axios({
    url: `${BASE_URL}/api/workout-exercises`,
    method: "POST",
    data: {
      name,
      order,
      exercise_id,
      count,
      count_type,
    },
  });
}
