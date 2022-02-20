"use strict";
const $saveBtn = $("#save-rft");
let $rounds = +$("#rounds").val();

$("#rounds").change(function () {
  $rounds = +$("#rounds").val();
  localStorage.setItem("rounds", JSON.stringify($rounds));
});

$saveBtn.on("click", async function () {
  let stages = $rounds;
  let stage_time = 0;

  postWorkout(stages, stage_time);

  for (let i = 0; i < excList.length; i++) {
    let order = i + 1;
    let exercise_id = excList[i].id;

    postWorkoutExercises(order, exercise_id);
  }
  localStorage.clear();
  window.location.href = `${BASE_URL}/`;
});
