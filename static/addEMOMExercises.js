"use strict";
const $saveBtn = $("#save-emom");
let $workoutLength = +$("#time").val();

//Listen for changes in workout length
$("#time").change(function () {
  $workoutLength = +$("#time").val();
  localStorage.setItem("time", JSON.stringify($workoutLength));
  if (excList.length > $workoutLength) {
    $selectedList.empty();
    excList = excList.slice(0, $workoutLength);
    localStorage.setItem("excList", JSON.stringify(excList));
    fillExercises();
  }
});

$saveBtn.on("click", async function () {
  let stages = excList.length;
  let stage_time = $workoutLength;

  await postWorkout(stages, stage_time);

  let index = 0;
  let minute = 1;
  while (minute <= $workoutLength) {
    let order = minute;
    let exercise_id = excList[index].id;

    await postWorkoutExercises(order, exercise_id);

    minute = minute + 1;
    index = (index + 1) % excList.length;
  }
  localStorage.clear();
  window.location.href = `${BASE_URL}/`;
});
