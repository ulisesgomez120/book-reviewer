$("#toggle").click(function() {
  if (
    $(this)
      .text()
      .toLowerCase() === "sign-in"
  ) {
    $(this).text("Sign-up");
  } else {
    $(this).text("Sign-in");
  }
  $("#login").toggle();
  $("#register").toggle();
});
