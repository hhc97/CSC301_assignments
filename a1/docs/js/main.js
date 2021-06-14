'use strict';

const imgPath = "images/cancel.png"

const add = document.querySelector('#addButton');
const inName = document.querySelector('#name');
const inCost = document.querySelector('#cost');
const cart = document.querySelector('#cart');

add.addEventListener('click', addItem);
cart.addEventListener('click', removeItem);

let worldId = 0;
let items = [];

var Item = function (name, cost) {
  this.id = worldId;
  worldId++;
  this.name = name;
  this.cost = cost;
}

function addItem(e) {
  e.preventDefault();
  const name = inName.value;
  const cost = parseFloat(inCost.value);
  if (name === "") {
    window.alert("Please enter an item name in the Name Field");
  } else if (cost !== "" && !isNaN(cost)) {
    const newItem = new Item(name, cost)
    items.push(newItem);
    addCartEntry(newItem.id, name, cost);
    updateTotals();
    inName.value = "";
    inCost.value = "";
  } else {
    window.alert("Please enter a numeric value in the Cost Field");
  }
}

function addCartEntry(newId, newName, newCost) {
  const empty = document.getElementById('emptyMessage');
  if (empty != null) {
    empty.remove();
  }
  const newEntry = document.createElement('li');
  newEntry.appendChild(document.createTextNode("$" + newCost.toFixed(2) + ' | ' + newName));
  newEntry.setAttribute("id", newId);
  const cancelButton = document.createElement('img');
  cancelButton.src = imgPath;
  cancelButton.setAttribute("id", "cancel")
  newEntry.appendChild(cancelButton);
  cart.appendChild(newEntry);
}

function updateTotals() {
  let total = 0;
  for (let i = 0; i < items.length; i++) {
    total = total + items[i].cost;
  }
  if (total < 0) {
    total = 0;
  }
  document.querySelector('#sum1').innerHTML = "Total before Tax: $" + total.toFixed(2);
  document.querySelector('#sum2').innerHTML = "Tax (13%): $" + (total * 0.13).toFixed(2);
  document.querySelector('#sum3').innerHTML = "Total: $" + (total * 1.13).toFixed(2);
}

function removeItem(e) {
  if (e.target.id === "cancel") {
    const removeId = parseInt(e.target.parentElement.id);
    for (let i = 0; i < items.length; i++) {
      if (removeId === items[i].id) {
        items.splice(i, 1);
        break;
      }
    }
    e.target.parentElement.remove();
    updateTotals();
  }
}
