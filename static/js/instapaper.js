$(document).ready(function () {
  $("#syncInstapaper").click(function(e) {
    e.preventDefault();

    // Prevent autofill from adding username/password to the form
    $("form#instapaperLoginForm #id_username").val("");
    $("form#instapaperLoginForm #id_password").val("");

    var oauthCached = $("#id_oauth_cached").is(":checked");
    if (oauthCached) {
      // Submit the form directly
      $("form#instapaperLoginForm").submit();
    } else {
      // Open the modal window for the user to login.
      $("#instapaperLoginModal").modal();
    }
    return false;
  });

  // Handle Instapaper use-cached-access-token checkbox
  $("input#id_oauth_cached").change(function() {
    var cached = $(this).is(':checked');
    $("input#id_username").prop("disabled", cached);
    $("input#id_password").prop("disabled", cached);
  });

  $("#clearInstapaperLoginForm").click(function(e) {
    e.preventDefault();

    // Prevent autofill from adding username/password to the form
    $("form#instapaperLoginForm #id_username").val("");
    $("form#instapaperLoginForm #id_password").val("");

    return false;
  });
});