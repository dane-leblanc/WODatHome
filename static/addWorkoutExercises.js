"use strict";
const $container = $(".container-workout");
const BASE_URL = "http://127.0.0.1:5000/api";
const $selectedList = $("#selected-exercises");

$container.on("click", ".btn-success", async function (e) {
  e.preventDefault();

  let exerciseId = +$(e.target).attr("data-id");
  console.log(exerciseId);
  let exercise = await axios.get(`${BASE_URL}/exercises/${exerciseId}`);
  let exerciseName = exercise.data.exercise.name;
  console.log(exerciseName);

  let $added_exercise = $(`<li data-id = ${exerciseId}> ${exerciseName}</li>`);
  $added_exercise.appendTo($selectedList);
});
