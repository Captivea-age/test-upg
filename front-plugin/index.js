// The Front object is loaded through the Front script added in the header of the main HTML.

// This keeps track of if Front has returned a conversation to the plugin.
let hasConversation;
let logged = false;
let accessToken = null;
let contactInfoLocations = [];
// const api = "https://comfortmonster.odoo.com";
// const api = "https://comfortmonster-thomas2-3997400.dev.odoo.com";

const groupBy = (key) => (array) =>
  array.reduce((objectsByKeyValue, obj) => {
    const value = obj[key];
    objectsByKeyValue[value] = (objectsByKeyValue[value] || []).concat(obj);
    return objectsByKeyValue;
  }, {});

Front.contextUpdates.subscribe((context) => {
  if (window.localStorage.getItem("logged")) {
    switch (context.type) {
      case "noConversation":
        // Set the conversation state.
        hasConversation = false;
        // Display `No Contact` data and clear the notes and set the tab to 'Info'.
        displayContactInfo();
        displayLocations();
        break;
      case "singleConversation":
        // Set the conversation state.
        hasConversation = true;
        // Load the Contact information based off of the event data. And set tab to 'Info'.
        document.getElementById("mainTitle").innerHTML =
          context.conversation.inboxes[0].name;

        loadContact(context.conversation.recipient);

        if (context.conversation.recipient.name) {
          const el = document.getElementById("searchForNameInstead");
          el.style.display = "block";
          el.href =
            api +
            "/web#action=138&model=res.partner&view_type=kanban&cids=1&menu_id=100&name=" +
            context.conversation.recipient.name;
        } else {
          document.getElementById("searchForNameInstead").style.display =
            "none";
        }

        break;
      default:
        break;
    }
  }
});

// Asynchronously loads the contact through our mocked CRM service once the body of the plugin is loaded.
async function loadContact(contact) {
  // Build and display our CRM data.
  const crmData = await queryCRM(contact);
  // Display Front contact info.
  if (crmData.contactInfo != null) {
    displayContactInfo(
      crmData.contactInfo.name,
      crmData.contactInfo.top_address,
      crmData.contactInfo.phone_sms,
      crmData.contactInfo.email,
      crmData.contactInfo.phone_1,
      crmData.contactInfo.phone_2
    );

    document.getElementById(
      "external-link"
    ).href = `${api}/web#id=${crmData.contactInfo.id}&action=138&model=res.partner&view_type=form&cids=1&menu_id=100`;
    //  Load the locations from our CRM data.

    contactInfoLocations = crmData.contactInfo.locations;

    displayLocations(crmData.locations, contactInfoLocations);
  } else {
    let locations = document.getElementById("locations");
    locations.innerHTML = "";
    displayContactInfo();
  }
}

// Displays Front contact information.
function displayContactInfo(
  name = "No Contact Found",
  top_address = "",
  phone_sms = "",
  email = "",
  phone_1 = "",
  phone_2 = ""
) {
  const nameElement = document.getElementById("name");
  const residentElement = document.getElementById("resident_title");
  const topAddressElement = document.getElementById("top_address");
  const phoneSmsElement = document.getElementById("phone_sms");
  const emailElement = document.getElementById("email");
  const phone1Element = document.getElementById("phone_1");
  const phone2Element = document.getElementById("phone_2");

  nameElement.textContent = name;

  if (name === "No Contact Found") {
    document.getElementById("locationsHistory").style.display = "none";
    document.getElementById("createNewCustomerContact").style.display = "block";
  } else {
    document.getElementById("locationsHistory").style.display = "block";
    document.getElementById("createNewCustomerContact").style.display = "none";
    document.getElementById("searchForNameInstead").style.display = "none";
  }

  if (top_address !== null) {
    if (top_address.length === 0) {
      residentElement.textContent = "";
    } else {
      residentElement.textContent = "Residential";
    }
  } else {
    residentElement.textContent = "";
  }
  topAddressElement.textContent = top_address;
  phoneSmsElement.textContent = phone_sms;
  emailElement.textContent = email;
  phone1Element.textContent = phone_1;
  phone2Element.textContent = phone_2;
}

// Displays the CRM locations.
function displayLocations(locations_list, all_locations, filter) {
  let location_name_list = [];
  let locations = document.getElementById("locations");
  locations.innerHTML = "";

  if (!all_locations) {
    locations = document.getElementById("locations");
    locations.innerHTML = "";
    return;
  }

  if (Array.isArray(all_locations)) {
  } else {
    location_name_list.push(all_locations.x_studio_location.name);
  }
  const groupByAddress = groupBy("x_studio_location_name");

  //if no tasks coming
  if (Object.entries(locations_list[0]).length === 0) {
    displayLocationWithoutTask(
      location_name_list,
      all_locations.x_studio_location.id,
      filter
    );
    return;
  }

  const grouped_locations_list = groupByAddress(locations_list[0]);

  // locations.innerHTML = "";

  Object.values(grouped_locations_list).forEach((location_task_list) => {
    if (location_task_list !== null || location_task_list !== undefined) {
      const indexOfLocation = location_name_list.indexOf(
        location_task_list[0].x_studio_location_name
      );

      if (indexOfLocation > -1) {
        location_name_list.splice(indexOfLocation, 1);
      }
      displayLocation(
        location_task_list,
        location_task_list[0].partner_id.id,
        filter
      );
    }
    //  return true;
  });
  displayLocationWithoutTask(
    location_name_list,
    all_locations.x_studio_location.id,
    filter
  );
}

function displayLocationWithoutTask(location_name_list, locationId, filter) {
  location_name_list.forEach((location_name) => {
    let locations = document.getElementById("locations");

    let location = document.createElement("div");

    let address_title = document.createElement("p");
    address_title.classList.add("address", "bold", "with-btn");

    let arrow = document.createElement("span");
    arrow.classList.add("arrow");
    let arrow_img = document.createElement("img");
    arrow_img.src = "images/right-arrow.png";
    arrow.appendChild(arrow_img);

    let address = document.createElement("span");
    address.textContent = location_name;

    let action_btn = document.createElement("span");
    action_btn.classList.add("action-btn");

    let action_external = document.createElement("a");
    action_external.target = "_blank";
    action_external.href = `${api}/web#id=${locationId}&cids=1&menu_id=100&model=res.partner&view_type=form`;
    let action_external_img = document.createElement("i");
    action_external_img.classList.add("fas", "fa-external-link-square-alt");
    action_external.appendChild(action_external_img);

    let action_link = document.createElement("a");
    action_link.href = "#";
    let action_link_img = document.createElement("img");
    action_link_img.src = "images/link.png";
    // action_link.appendChild(action_link_img);

    action_btn.appendChild(action_external);
    action_btn.appendChild(action_link);

    address_title.appendChild(arrow);
    address_title.appendChild(address);
    address_title.appendChild(action_btn);

    if (!filter) {
      location.appendChild(address_title);
    }

    locations.appendChild(location);
  });
}

function displayLocation(location_task_list, locationId, filter) {
  const location_obj = location_task_list[0];
  let locations = document.getElementById("locations");

  let location = document.createElement("div");

  let address_title = document.createElement("p");
  address_title.classList.add("address", "bold", "with-btn");
  address_title.id = "locationAddress";

  let arrow = document.createElement("span");
  arrow.classList.add("arrow");
  let arrow_img = document.createElement("i");
  arrow_img.classList.add("fas", "fa-long-arrow-alt-right");
  arrow.appendChild(arrow_img);

  let address = document.createElement("span");
  address.textContent = contactInfoLocations.x_studio_location.name;

  let action_btn = document.createElement("span");
  action_btn.classList.add("action-btn");

  let action_external = document.createElement("a");
  action_external.target = "_blank";
  action_external.href = `${api}/web#id=${locationId}&cids=1&menu_id=100&model=res.partner&view_type=form`;
  let action_external_img = document.createElement("i");
  action_external_img.classList.add("fas", "fa-external-link-square-alt");
  action_external.appendChild(action_external_img);

  let action_link = document.createElement("a");
  action_link.href = "#";
  let action_link_img = document.createElement("img");
  action_link_img.src = "images/link.png";
  // action_link.appendChild(action_link_img);

  action_btn.appendChild(action_external);
  action_btn.appendChild(action_link);

  address_title.appendChild(arrow);
  address_title.appendChild(address);
  address_title.appendChild(action_btn);

  if (!document.getElementById("locationAddress")) {
    location.appendChild(address_title);
  }

  let tasks = document.createElement("div");
  displayTask(location_task_list).forEach((task) => {
    tasks.appendChild(task);
  });

  locations.appendChild(location);
  locations.appendChild(tasks);
}

function displayTask(location_task_list) {
  let tasks = location_task_list.map((task_obj) => {
    let task = document.createElement("div");
    task.classList.add("task");
    let task_title = document.createElement("p");
    task_title.classList.add("title", "side-heading", "with-btn");

    const status = `<span class="task-status">${task_obj.stage_id.name}</span>`;

    let title = document.createElement("span");
    title.style.flex = "1";

    const dateHDtask = task_obj.create_date
      ? `<br><span class="task-date">${task_obj.create_date
          .split(":")
          .slice(0, -1)
          .join(":")}</span>`
      : "";

    const dateFStask = task_obj.planned_date_begin
      ? `<br><span class="task-date">${task_obj.planned_date_begin
          .split(":")
          .slice(0, -1)
          .join(":")}</span>`
      : "";

    title.innerHTML =
      (task_obj.helpdesk_ticket_id ? " J" : " HD") +
      task_obj.id +
      (!task_obj.x_studio_department
        ? " - " + task_obj.display_name
        : " - " + task_obj.x_studio_department.display_name) +
      dateHDtask +
      dateFStask +
      status;

    let action_btn = document.createElement("span");
    action_btn.classList.add("action-btn", "action-task-btn");

    let action_external = document.createElement("a");
    action_external.href = task_obj.helpdesk_ticket_id
      ? `${api}/web#id=${task_obj.id}&action=335&active_id=${task_obj.partner_id.id}&model=project.task&view_type=form&cids=1&menu_id=100`
      : `${api}/web#id=${task_obj.id}&active_id=${task_obj.partner_id.id}&model=helpdesk.ticket&view_type=form&cids=1&menu_id=100`;
    action_external.target = "_blank";
    let action_external_img = document.createElement("i");
    action_external_img.classList.add("fas", "fa-external-link-square-alt");
    action_external.appendChild(action_external_img);

    let action_link = document.createElement("a");
    action_link.href = "#";
    let action_link_img = document.createElement("img");
    action_link_img.src = "images/link.png";
    // action_link.appendChild(action_link_img);

    let expand_btn = document.createElement("span");
    expand_btn.innerHTML = "+";
    expand_btn.classList.add("expand-btn");

    action_btn.appendChild(action_external);
    action_btn.appendChild(action_link);

    task_title.appendChild(expand_btn);
    task_title.appendChild(title);
    task_title.appendChild(action_btn);

    let detail = document.createElement("p");
    detail.classList.add("detail");
    detail.innerHTML = task_obj.description;

    //"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.";

    task.appendChild(task_title);
    task.appendChild(detail);

    detail.style["max-height"] = "0%";

    task_title.addEventListener("click", () => {
      if (detail.style["max-height"] === "100%") {
        detail.style["max-height"] = "0%";
        expand_btn.innerHTML = "+";
      } else {
        detail.style["max-height"] = "100%";
        expand_btn.innerHTML = "-";
      }
    });

    return task;
  });
  return tasks;
}

function displayTasks(locations_list) {
  let location_name_list = [];
  let locations = document.getElementById("locations");
  locations.innerHTML = "";

  const groupByAddress = groupBy("x_studio_location_name");

  //if no tasks coming
  if (Object.entries(locations_list[0]).length === 0) {
    return;
  }

  const grouped_locations_list = groupByAddress(locations_list[0]);
  Object.values(grouped_locations_list).forEach((location_task_list) => {
    if (location_task_list !== null || location_task_list !== undefined) {
      const indexOfLocation = location_name_list.indexOf(
        location_task_list[0].x_studio_location_name
      );

      if (indexOfLocation > -1) {
        location_name_list.splice(indexOfLocation, 1);
      }
      displayLocation(location_task_list, location_task_list[0].partner_id.id);
    }
    //  return true;
  });
}

//Login
async function login() {
  // Build and display our CRM data.
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  try {
    const res = await queryLogin(email, password);
    window.localStorage.setItem("accessToken", res.data.access_token);
    window.localStorage.setItem("logged", true);

    checkAuth();

    logged = true;
  } catch (e) {
    window.localStorage.removeItem("logged");
    console.error(e);
  }
}

function checkAuth() {
  const container = document.querySelector(".container");
  const loginForm = document.querySelector(".login-form");

  if (window.localStorage.getItem("logged")) {
    container.classList.remove("displayNone");
    loginForm.classList.add("displayNone");
  } else {
    container.classList.add("displayNone");
    loginForm.classList.remove("displayNone");
  }
}

checkAuth();

document.getElementById("login").addEventListener("click", () => {
  login();
});

document.getElementById("logout").addEventListener("click", () => {
  window.localStorage.removeItem("accessToken");
  window.localStorage.removeItem("logged");
  checkAuth();
});

Array.from(document.getElementsByClassName("filter")).forEach((el) => {
  el.addEventListener("click", (e) => {
    e.preventDefault();
    const filter = e.target.getAttribute("data-filter");

    Array.from(document.getElementsByClassName("filter")).forEach((el) => {
      el.classList.remove("active");
    });

    el.classList.add("active");

    let locations = document.getElementById("locations");
    locations.innerHTML = "";

    getProjectTasks(filter)
      .then((response) => {
        let locations = response.data.results;

        displayLocations([locations], contactInfoLocations, true);
      })
      .catch((e) => {
        console.log(e);
      });
  });
});
