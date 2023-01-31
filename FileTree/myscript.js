function traverse(node, root, sp) {
  for (var child in node) {
    for (var key in node[child]) {
      if (!node[child].hasOwnProperty(key)) {
        continue;
      }
      if (key == "type" && node[child][key] == "d") {
        ldiv = document.createElement("div");
        ldiv.className = "check";
        ldiv.setAttribute("style", `margin-left: ${sp*10}px`);
        ldiv.innerHTML = `<input type="checkbox"><label>${node[child]["name"]}</label>`
        root.appendChild(ldiv);
        traverse(node[child]["child"], ldiv, sp+1);
      } else if (key == "type" && node[child][key] == "f") {
        ldiv = document.createElement("div");
        ldiv.className = "check";
        ldiv.setAttribute("style", `margin-left: ${sp*10}px`);
        ldiv.innerHTML = `<input type="checkbox"><label>${node[child]["name"]}</label>`
        root.appendChild(ldiv);
      }
    }
  }
}

function checkboxParentAll(elem, bool) {
  var pelem = elem.parentNode;
  var childCheck = pelem.children;
  for (var i = 0; i < childCheck.length; i++) {
    if (childCheck[i].tagName == "INPUT") {
      childCheck[i].checked = bool;
    } else if (childCheck[i].tagName == "DIV") {
      checkboxChildAll(childCheck[i], bool);
    }
  }
}

function checkboxChildAll(elem, bool) {
  var childCheck = elem.children;
  for (var i = 0; i < childCheck.length; i++) {
    if (childCheck[i].tagName == "INPUT") {
      childCheck[i].checked = bool;
    } else if (childCheck[i].tagName == "DIV") {
      checkboxChildAll(childCheck[i], bool);
    }
  }
}

async function fetchRequestWithError() {
  try {
    const url = "http://localhost:8080/mytree.json";
    const response = await fetch(url);
    if (response.status >= 200 && response.status < 400) {
      const data = await response.json();
      var root = document.getElementById("maintree");
      traverse(data, root, 0);
      var checks = document.querySelectorAll("input[type=checkbox]");
      for (var i = 0; i < checks.length; i++) {
        checks[i].addEventListener('change', function() {
          if (this.checked) {
            checkboxParentAll(this, true);
          } else {
            checkboxParentAll(this, false);
          }
        })
      }
    }
  } catch (error) {
    // Generic error handler
    console.log(error);
  }
}

fetchRequestWithError();
