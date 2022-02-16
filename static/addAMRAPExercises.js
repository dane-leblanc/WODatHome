"use strict";
const $container = $(".container-workout");
const BASE_URL = "http://127.0.0.1:5000";
const $selectedList = $("#selected-exercises");
const $clearBtn = $("#clear-button");
const $saveBtn = $("#save-amrap");
let excList = [];
let $stagesVal = +$("#stages").val();
let $excPerStageVal = +$("#exc-per-stage").val();
let $stageTime = +$("#stage-time").val();

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
  fillStages();
}

//Listen for changes in AMRAP form
$("#stages").change(function () {
  $selectedList.empty();
  $stagesVal = +$("#stages").val();
  localStorage.setItem("stages", JSON.stringify($stagesVal));
  if (excList.length > $stagesVal * $excPerStageVal) {
    excList = excList.slice(0, $stagesVal * $excPerStageVal);
  }
  localStorage.setItem("excList", JSON.stringify(excList));
  setStages();
  fillStages();
});

$("#exc-per-stage").change(function () {
  $selectedList.empty();
  $excPerStageVal = +$("#exc-per-stage").val();
  localStorage.setItem("excPerStage", JSON.stringify($excPerStageVal));
  if (excList.length > $stagesVal * $excPerStageVal) {
    excList = excList.slice(0, $stagesVal * $excPerStageVal);
  }
  localStorage.setItem("excList", JSON.stringify(excList));
  setStages();
  fillStages();
});

//Add exercise to exercise list
$container.on("click", ".btn-success", function (e) {
  if ($stagesVal * $excPerStageVal == excList.length) {
    return alert("You cannot add another exercise.");
  }
  let exerciseId = +$(e.target).attr("data-id");
  let exerciseName = $(e.target).attr("data-name");
  let newExc = {
    id: exerciseId,
    name: exerciseName,
  };
  if (excList.length <= $stagesVal * $excPerStageVal) {
    excList.push(newExc);
    localStorage.setItem("excList", JSON.stringify(excList));
  }
  let index = excList.length - 1;
  addExercise(newExc, index);
});

$container.on("dblclick", ".li-exercise", function (e) {
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

$clearBtn.on("click", function () {
  localStorage.clear();
  location.reload();
});
$("nav").on("click", "a", function () {
  localStorage.clear();
});

$saveBtn.on("click", async function () {
  if ($stagesVal * $excPerStageVal != excList.length) {
    return alert(
      `Please add ${
        $stagesVal * $excPerStageVal - excList.length
      } more exercise(s).`
    );
  } else {
    //Store workout in db
    let type = "AMRAP";
    let name = $("#workout-name").text();
    let username = $("#workout-name").attr("data-user");
    let stages = $stagesVal;
    let stage_time = +$("#stage-time").val();

    const workoutRes = await axios({
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

    //Store workout exercises in db
    excList = addRests(excList);

    for (let i = 0; i < excList.length; i++) {
      let order = i + 1;
      let exercise_id = excList[i].id;
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
    localStorage.clear();
    window.location.href = `${BASE_URL}/`;
  }
});

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
    addExercise(exc, index);
    index = index + 1;
  }
}

function addExercise(exc, index) {
  let $newLi = $(
    `<li class = "li-exercise form-inline" data-id = ${exc.id}> ${exc.name}</li>`
  );
  let currStage = Math.floor(index / $excPerStageVal) + 1;
  $newLi.appendTo(`.stage-${currStage}`);
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

function addRests(excList) {
  let rest = {
    id: 500,
    name: "Rest",
  };
  for (
    let i = excList.length - $excPerStageVal;
    i > 0;
    i = i - $excPerStageVal
  ) {
    excList.splice(i, 0, rest);
  }
  return excList;
}
