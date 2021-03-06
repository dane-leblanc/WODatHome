"use strict";
const $saveBtn = $("#save-amrap");
let $stagesVal = +$("#stages").val();
let $excPerStageVal = +$("#exc-per-stage").val();
let $stageTime = +$("#stage-time").val();
let $restTime = +$("#rest-time").val();

//Listen for changes in AMRAP form
$("#rest-time").change(function () {
  $restTime = +$("#rest-time").val();
  localStorage.setItem("restTime", $restTime);
});

$("#stage-time").change(function () {
  $stageTime = +$("#stage-time").val();
  localStorage.setItem("stageTime", $stageTime);
});

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

$saveBtn.on("click", async function () {
  if ($stagesVal * $excPerStageVal != excList.length) {
    $(".alert").remove();
    let $addAlert = $(
      `<div class='alert alert-danger' role='alert'>Please add ${
        $stagesVal * $excPerStageVal - excList.length
      } more exercise(s).</div>`
    );
    $addAlert.fadeIn("slow").delay(2500).hide(0);
    $addAlert.appendTo($selectedList);
    return;
  } else {
    let stages = $stagesVal;
    let stage_time = +$("#stage-time").val();

    await postWorkout(stages, stage_time);

    excList = addRests(excList);

    for (let i = 0; i < excList.length; i++) {
      let order = i + 1;
      let exercise_id = excList[i].id;

      await postWorkoutExercises(order, exercise_id);
    }
    localStorage.clear();
    window.location.href = `${BASE_URL}/`;
  }
});

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
