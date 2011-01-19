function loaded() {
  if (document.location.hash) {
    document.forms[0].access_token.value = document.location.hash.match(/#access_token=([^&]*)/)[1];
    document.forms[0].submit()
  } else {
    top.location.href = 'https://graph.facebook.com/oauth/authorize?client_id=156562204392783&type=user_agent&redirect_uri=' + document.location +'&scope=offline_access%2Cuser_photo_video_tags';
  }
}
