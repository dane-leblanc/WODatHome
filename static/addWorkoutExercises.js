"use strict";
const $container = $(".container-workout");
const BASE_URL = "http://127.0.0.1:5000/api";
const $selectedList = $("#selected-exercises");

if (window.location.href.indexOf("/create/AMRAP/") != -1) {
  const excList = [];
  let $excPerStage = +$("#exc-per-stage").val();
  setStages();
  $("#stages").change(function () {
    $selectedList.empty();
    setStages();
  });
  $container.on("click", ".btn-success", async function (e) {
    e.preventDefault();
    let exerciseId = +$(e.target).attr("data-id");
    excList.push(exerciseId);
    let exercise = await axios.get(`${BASE_URL}/exercises/${exerciseId}`);
    let exerciseName = exercise.data.exercise.name;
    let $added_exercise = $(
      `<li data-id = ${exerciseId}> ${exerciseName}</li>`
    );
    console.log(exerciseId);
    console.log($excPerStage);
    if (excList.indexOf(exerciseId) < $excPerStage) {
      $added_exercise.appendTo($(".stage-1"));
    }
  });
  function setStages() {
    let $stages = $("#stages").val();
    for (let i = 1; i <= +$stages; i++) {
      $(`<li>`).text(`Stage ${i}`).appendTo($selectedList);
      $(`<ul>`).attr("class", `stage-${i}`).appendTo($selectedList);
    }
  }
}
