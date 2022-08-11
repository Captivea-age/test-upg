//This function returns CRM data of customer and tasks

// const api = "https://comfortmonster.odoo.com";
const api = "https://comfortmonster-staging.odoo.com";
let locationId;

function queryCRM({ contact, handle }, accessToken) {
  return new Promise(function (resolve) {
    //get rsource by email
    //email = "admin@example.com";

    let contactInfo = null;
    let locations = [];
    let isPhone = false;
    let searchValue = encodeURIComponent(handle);

    if (contact) {
      isPhone = contact.handles[0].type === "phone";

      if (isPhone) {
        searchValue = encodeURIComponent(
          formatPhoneNumber(handle.replace("+", ""))
        );
      }
    }

    axios
      .get(
        api +
          "/api/res.partner?filters=" +
          "[('" +
          (contact ? (isPhone ? "phone" : "email") : "email") +
          "', '=', '" +
          searchValue +
          "')]&include_fields=['name','id','phone','mobile','email','x_studio_extra_phone_numbers','contact_address','contact_address_complete','display_name',('x_studio_one2many_field_6JWoi',('id',('x_studio_location',('name','id'))))]",
        {
          headers: {
            // "Access-Control-Allow-Origin": "*",
            // "Access-Control-Allow-Methods": "GET,OPTIONS",
            //"Access-Control-Request-Headers": "Access-Token",
            "Access-Token": localStorage.getItem("accessToken")
            // "Access-Token": "2d06dde9c2281805d962164ba7acd0ab234f0511"
          }
        }
      )
      .then(function (response) {
        // set information of customer
        const customer = response.data.results[0];
        if (customer != null) {
          contactInfo = {
            id: customer.id,
            name: customer.name,
            top_address: customer.contact_address_complete,
            phone_sms: customer.phone,
            email: customer.email,
            phone_1: customer.mobile,
            phone_2: customer.x_studio_extra_phone_numbers,
            locations: customer.x_studio_one2many_field_6JWoi
          };

          if (!contactInfo.locations) {
            resolve({ locations, contactInfo });
            return;
          }

          const customer_id = customer.id;
          //const customer_id = 21380; //21380; //125775
          locationId = contactInfo.locations.x_studio_location.id;
          // get locations information of the client: ('state_id',('code'))

          let locationsE = document.getElementById("locations");
          locationsE.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';

          axios
            .get(
              api +
                "/api/project.task?filters=[('is_fsm','=','True'),('partner_id.id','='," +
                locationId +
                ")]&include_fields=[('stage_id', ('name')),'planned_date_end',('helpdesk_ticket_id', ('id')),('partner_id',('id')),'x_studio_location_name','planned_date_begin','description',('x_studio_job_type_id',('id','display_name')),'planned_date_begin',('x_studio_department',('id','display_name'))]",
              {
                headers: {
                  "Access-Token": localStorage.getItem("accessToken")
                }
              }
            )
            .then(function (response) {
              locations.push(response.data.results);
              resolve({ locations, contactInfo });
            })
            .catch(function (error, contactInfo) {
              console.log(error);
            });
        } else {
          console.log("in else condition");
          resolve({ locations, contactInfo });
        }
      })
      .catch(function (error, contactInfo) {
        // handle error
        contactInfo = {
          name: "",
          top_address: "",
          phone_sms: "",
          email: "",
          phone_1: "",
          phone_2: "",
          locations: []
        };
        console.log(error);
        window.localStorage.removeItem("logged");
        checkAuth();
      });
  });
}

function queryLogin(username, password) {
  return axios.get(api + "/api/auth/get_tokens", {
    params: {
      username,
      password
    }
  });
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

function formatPhoneNumber(phoneNumberString) {
  var cleaned = ("" + phoneNumberString).replace(/\D/g, "");
  var match = cleaned.match(/^(1|)?(\d{3})(\d{3})(\d{4})$/);
  if (match) {
    var intlCode = match[1] ? "+1 " : "";
    return [intlCode, match[2], "-", match[3], "-", match[4]].join("");
  }
  return null;
}

async function getProjectTasks(filter) {
  let filterQuery = "";

  let locations = document.getElementById("locations");
  locations.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';

  switch (filter) {
    case "hd": {
      return axios
        .get(
          api +
            "/api/helpdesk.ticket?filters=[" +
            "('partner_id.id','='," +
            locationId +
            ")]&include_fields=['create_date',('stage_id', ('name')),('partner_id',('id')),'description', 'display_name']",
          {
            headers: {
              "Access-Token": localStorage.getItem("accessToken")
            }
          }
        )
        .catch((e) => {
          if (e.response.status === 401) {
            window.localStorage.removeItem("logged");
            checkAuth();
          }
        });
    }
    case "fs": {
      filterQuery = "('is_fsm','=','True'),";

      return axios
        .get(
          api +
            "/api/project.task?filters=[" +
            filterQuery +
            "('partner_id.id','='," +
            locationId +
            ")]&include_fields=[('stage_id', ('name')),'planned_date_end',('helpdesk_ticket_id', ('id','name', 'description')),('partner_id',('id')),'x_studio_location_name','planned_date_begin','description',('x_studio_job_type_id',('id','display_name')),'planned_date_begin',('x_studio_department',('id','display_name'))]",
          {
            headers: {
              "Access-Token": localStorage.getItem("accessToken")
            }
          }
        )
        .catch((e) => {
          if (e.response.status === 401) {
            window.localStorage.removeItem("logged");
            checkAuth();
          }
        });
    }
    default: {
      return new Promise(async (resolve) => {
        const hd = await axios
          .get(
            api +
              "/api/helpdesk.ticket?filters=[" +
              "('partner_id.id','='," +
              locationId +
              ")]&include_fields=['create_date',('stage_id', ('name')),('partner_id',('id')),'description', 'display_name']",
            {
              headers: {
                "Access-Token": localStorage.getItem("accessToken")
              }
            }
          )
          .catch((e) => {
            if (e.response.status === 401) {
              window.localStorage.removeItem("logged");
              checkAuth();
            }
          });

        filterQuery = "('is_fsm','=','True'),";

        const fs = await axios
          .get(
            api +
              "/api/project.task?filters=[" +
              filterQuery +
              "('partner_id.id','='," +
              locationId +
              ")]&include_fields=['planned_date_end',('stage_id', ('name')),('helpdesk_ticket_id',('id','name', 'description')),('partner_id',('id')),'x_studio_location_name','planned_date_begin','description',('x_studio_job_type_id',('id','display_name')),'planned_date_begin',('x_studio_department',('id','display_name'))]",
            {
              headers: {
                "Access-Token": localStorage.getItem("accessToken")
              }
            }
          )
          .catch((e) => {
            if (e.response.status === 401) {
              window.localStorage.removeItem("logged");
              checkAuth();
            }
          });

        resolve({
          data: { results: [...hd.data.results, ...fs.data.results] }
        });
      });
    }
  }
}
