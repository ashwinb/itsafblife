function loaded() {
  if (document.location.hash) {
    document.forms[0].access_token.value = document.location.hash.substr(1);
    document.forms[0].submit()
  }
}
