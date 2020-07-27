async function submit_button(evt) {
  evt.preventDefault()
  console.log("this is submit_box ", $("#submit_box").val())
  response = `{submit_word:"${$("#submit_box").val()}"}`
  console.log(response)
  await axios.post("/api/score-word", {submit_word:$("#submit_box").val()})
}
$("#submit_form").on("submit", submit_button)