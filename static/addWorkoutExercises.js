"use strict";
const $container = $(".container-workout");
const BASE_URL = "http://127.0.0.1:5000/api";
const $selectedList = $("#selected-exercises");
const $clearBtn = $("#clear-button");
let excList = [];
// Creating an AMRAP
if (window.location.href.indexOf("/create/AMRAP/") != -1) {
  let $stagesVal = +$("#stages").val();
  let $excPerStageVal = +$("#exc-per-stage").val();
  if (localStorage.excList) {
    for (let ex of JSON.parse(localStorage.excList)) {
      excList.push(ex);
    }
    setStages();
    fillStages();
  } else {
    setStages();
  }

  $("#stages").change(function () {
    $selectedList.empty();
    $stagesVal = +$("#stages").val();
    setStages();
    fillStages();
  });
  $("#exc-per-stage").change(function () {
    $selectedList.empty();
    $excPerStageVal = +$("#exc-per-stage").val();
    setStages();
    fillStages();
  });
  $container.on("click", ".btn-success", function (e) {
    e.preventDefault();
    let exerciseId = +$(e.target).attr("data-id");
    let exerciseName = $(e.target).attr("data-name");
    let newExc = { id: exerciseId, name: exerciseName };
    if (excList.length <= $stagesVal * $excPerStageVal) {
      excList.push(newExc);
      localStorage.clear();
      localStorage.setItem("excList", JSON.stringify(excList));
    }
    let $addedExercise = $(
      `<li class = "li-exercise" data-id = ${exerciseId}> ${exerciseName}</li>`
    );
    let currStage = Math.floor((excList.length - 1) / $excPerStageVal) + 1;
    $addedExercise.appendTo(`.stage-${currStage}`);
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
      let $newLi = $(
        `<li class = "li-exercise" data-id = ${exc.id}> ${exc.name}</li>`
      );
      let currStage = Math.floor(index / $excPerStageVal) + 1;
      $newLi.appendTo(`.stage-${currStage}`);
      index = index + 1;
    }
  }
  $clearBtn.on("click", function () {
    localStorage.clear();
    location.reload();
  });
  $("nav").on("click", "a", function () {
    console.log("clicked");
    localStorage.clear();
  });
}
