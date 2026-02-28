(() => {
  // pointless_impressions_src/theme/static_src/src/js/cart.js
  function getCsrfToken() {
    const tokenEl = document.querySelector("[name=csrfmiddlewaretoken]");
    return tokenEl ? tokenEl.value : "";
  }
  async function updateCartDropdownHTML() {
    const cartDropdown = document.getElementById("cart-dropdown-content");
    if (!cartDropdown) {
      console.warn("Cart dropdown element not found. Cannot update.");
      return;
    }
    try {
      const response = await fetch("/checkout/cart-dropdown/", {
        method: "GET",
        headers: {
          "X-Requested-With": "XMLHttpRequest"
        },
        credentials: "include"
      });
      if (!response.ok) {
        throw new Error(`Failed to fetch cart: ${response.status}`);
      }
      const data = await response.json();
      cartDropdown.innerHTML = data.html;
    } catch (error) {
      console.error("Error refreshing cart dropdown:", error);
      cartDropdown.innerHTML = '<div class="p-4 text-error">Could not load cart.</div>';
    }
  }
  function openCartDropdown() {
    const cartDropdown = document.getElementById("cart-dropdown-content");
    if (!cartDropdown) return;
    const dropdownContainer = cartDropdown.closest(".dropdown");
    if (dropdownContainer) {
      dropdownContainer.classList.add("dropdown-open");
      setTimeout(() => {
        dropdownContainer.classList.remove("dropdown-open");
      }, 3e3);
    }
  }
  function initCart() {
    updateCartDropdownHTML();
  }
  if (typeof window !== "undefined") {
    window.cart = {
      init: initCart,
      updateCartDropdownHTML,
      openCartDropdown
    };
  }
  document.addEventListener("DOMContentLoaded", () => {
    if (window.cart) {
      window.cart.init();
    }
  });

  // pointless_impressions_src/theme/static_src/src/js/checkout.js
  var card = null;
  var payments = null;
  var paymentInProgress = false;
  var delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
  async function refreshOrderSummary() {
    window.location.reload();
  }
  async function handleCartUpdate(form) {
    const formData = new FormData(form);
    const artworkId = form.querySelector('input[name="artwork_id"]').value;
    if (!artworkId) return;
    try {
      const response = await fetch("/checkout/update/", {
        method: "POST",
        headers: {
          "X-Requested-With": "XMLHttpRequest",
          "X-CSRFToken": getCsrfToken()
        },
        body: formData,
        credentials: "include"
      });
      const data = await response.json();
      if (data.success) {
        if (window.Toast) window.Toast.show(data.message, "success");
        await refreshOrderSummary();
      } else {
        if (window.Toast) window.Toast.show(data.error, "error");
      }
    } catch (err) {
      console.error("Failed to submit form:", err);
      if (window.Toast) window.Toast.show("Error updating cart.", "error");
    }
  }
  async function handleRemoveItem(artworkId) {
    try {
      const response = await fetch("/checkout/remove-item/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-Requested-With": "XMLHttpRequest",
          "X-CSRFToken": getCsrfToken()
        },
        body: JSON.stringify({ artwork_id: artworkId }),
        credentials: "include"
      });
      const data = await response.json();
      if (data.success) {
        window.location.reload();
      } else {
        if (window.Toast) window.Toast.show(data.error || "Failed to remove item.", "error");
      }
    } catch (err) {
      console.error("Failed to remove item:", err);
      if (window.Toast) window.Toast.show("Error removing item.", "error");
    }
  }
  function getSquareCardStyles() {
    const pointlessWhite = "#FAFAFA";
    const pointlessBlack = "#050505";
    const pointlessBlue = "#2563EB";
    return {
      ".input-container": {
        borderColor: pointlessBlue,
        borderRadius: "4px",
        borderWidth: "1px"
      },
      "input": {
        backgroundColor: pointlessWhite,
        color: pointlessBlack,
        fontSize: "16px"
      },
      "input::placeholder": {
        color: pointlessBlack
      },
      ".message-text": {
        color: "#ef4444"
      },
      ".message-icon": {
        color: "#ef4444"
      }
    };
  }
  async function initializeSquare() {
    const appIdElement = document.getElementById("square-app-id");
    const locIdElement = document.getElementById("square-location-id");
    if (!appIdElement || !locIdElement) {
      console.error("Square Credentials not found in DOM");
      return;
    }
    const appId = JSON.parse(appIdElement.textContent);
    const locationId = JSON.parse(locIdElement.textContent);
    try {
      if (!window.Square) {
        throw new Error("Square.js script not loaded");
      }
      payments = window.Square.payments(appId, locationId);
      const cardStyles = getSquareCardStyles();
      card = await payments.card({ style: cardStyles });
      await card.attach("#card-container");
    } catch (e) {
      console.error("Error initializing Square Payments:", e);
      if (window.Toast) window.Toast.show("Error initializing payment form.", "error");
    }
  }
  function getSelectText(id) {
    const el = document.getElementById(id);
    if (el && el.selectedIndex !== -1) {
      return el.options[el.selectedIndex].text;
    }
    return "";
  }
  function getValue(id) {
    const el = document.getElementById(id);
    return el ? el.value : "";
  }
  function validateCheckoutForm() {
    const errors = [];
    const checkoutForm = document.getElementById("checkout-form");
    if (!checkoutForm) {
      errors.push("Checkout form not found.");
      return errors;
    }
    const requiredShippingFields = [
      { id: "id_shipping_first_name", label: "Shipping First Name" },
      { id: "id_shipping_last_name", label: "Shipping Last Name" },
      { id: "id_shipping_address_line_1", label: "Shipping Address" },
      { id: "id_shipping_city", label: "Shipping City" },
      { id: "id_shipping_postcode", label: "Shipping Postcode" },
      { id: "id_shipping_country", label: "Shipping Country" }
    ];
    requiredShippingFields.forEach((field) => {
      const el = document.getElementById(field.id);
      if (!el || el.value.trim() === "") {
        errors.push(`${field.label} is required.`);
      }
    });
    const billingCheckbox = document.getElementById("id_billing_same_as_shipping");
    if (billingCheckbox && !billingCheckbox.checked) {
      const requiredBillingFields = [
        { id: "id_billing_first_name", label: "Billing First Name" },
        { id: "id_billing_last_name", label: "Billing Last Name" },
        { id: "id_billing_address_line_1", label: "Billing Address" },
        { id: "id_billing_city", label: "Billing City" },
        { id: "id_billing_postcode", label: "Billing Postcode" },
        { id: "id_billing_country", label: "Billing Country" }
      ];
      requiredBillingFields.forEach((field) => {
        const el = document.getElementById(field.id);
        if (!el || el.value.trim() === "") {
          errors.push(`${field.label} is required.`);
        }
      });
    }
    return errors;
  }
  function populateConfirmationModal() {
    const shipping = {
      firstName: getValue("id_shipping_first_name"),
      lastName: getValue("id_shipping_last_name"),
      line1: getValue("id_shipping_address_line_1"),
      line2: getValue("id_shipping_address_line_2"),
      city: getValue("id_shipping_city"),
      county: getValue("id_shipping_county"),
      postcode: getValue("id_shipping_postcode"),
      country: getSelectText("id_shipping_country")
    };
    const set = (id, val) => {
      const el = document.getElementById(id);
      if (el) el.textContent = val;
    };
    set("modal-shipping-first-name", shipping.firstName);
    set("modal-shipping-last-name", shipping.lastName);
    set("modal-shipping-line1", shipping.line1);
    set("modal-shipping-city", shipping.city);
    set("modal-shipping-postcode", shipping.postcode);
    set("modal-shipping-country", shipping.country);
    const line2Wrap = document.getElementById("modal-shipping-line2-wrapper");
    if (line2Wrap) line2Wrap.style.display = shipping.line2 ? "block" : "none";
    if (shipping.line2) set("modal-shipping-line2", shipping.line2);
    const countyWrap = document.getElementById("modal-shipping-county-wrapper");
    if (countyWrap) countyWrap.style.display = shipping.county ? "block" : "none";
    if (shipping.county) set("modal-shipping-county", shipping.county);
    const isSameAsShipping = document.getElementById("id_billing_same_as_shipping");
    let billing;
    if (isSameAsShipping && isSameAsShipping.checked) {
      billing = { ...shipping };
    } else {
      billing = {
        firstName: getValue("id_billing_first_name"),
        lastName: getValue("id_billing_last_name"),
        line1: getValue("id_billing_address_line_1"),
        line2: getValue("id_billing_address_line_2"),
        city: getValue("id_billing_city"),
        county: getValue("id_billing_county"),
        postcode: getValue("id_billing_postcode"),
        country: getSelectText("id_billing_country")
      };
    }
    set("modal-billing-first-name", billing.firstName);
    set("modal-billing-last-name", billing.lastName);
    set("modal-billing-line1", billing.line1);
    set("modal-billing-city", billing.city);
    set("modal-billing-postcode", billing.postcode);
    set("modal-billing-country", billing.country);
    const billingLine2Wrap = document.getElementById("modal-billing-line2-wrapper");
    if (billingLine2Wrap) billingLine2Wrap.style.display = billing.line2 ? "block" : "none";
    if (billing.line2) set("modal-billing-line2", billing.line2);
    const billingCountyWrap = document.getElementById("modal-billing-county-wrapper");
    if (billingCountyWrap) billingCountyWrap.style.display = billing.county ? "block" : "none";
    if (billing.county) set("modal-billing-county", billing.county);
  }
  function getFormattedShippingAddress() {
    const parts = [];
    const firstName = getValue("id_shipping_first_name");
    const lastName = getValue("id_shipping_last_name");
    const line1 = getValue("id_shipping_address_line_1");
    const line2 = getValue("id_shipping_address_line_2");
    const city = getValue("id_shipping_city");
    const county = getValue("id_shipping_county");
    const postcode = getValue("id_shipping_postcode");
    const country = getSelectText("id_shipping_country");
    if (firstName || lastName) parts.push(firstName + " " + lastName);
    if (line1) parts.push(line1);
    if (line2) parts.push(line2);
    if (city) parts.push(city);
    if (county) parts.push(county);
    if (postcode) parts.push(postcode);
    if (country) parts.push(country);
    return parts.join("<br>");
  }
  document.addEventListener("DOMContentLoaded", async function() {
    await initializeSquare();
    const placeOrderButton = document.getElementById("place-order-button");
    const confirmModal = document.getElementById("confirm-order-modal");
    const finalConfirmBtn = document.getElementById("modal-confirm-btn");
    const modalLoadingSpinner = document.getElementById("modal-loading-spinner");
    const checkoutForm = document.getElementById("checkout-form");
    const billingFields = document.getElementById("billing-fields-container");
    const billingConfirmationContainer = document.querySelector(".billing-confirmation-container");
    const billingCheckbox = document.getElementById("id_billing_same_as_shipping");
    const billingConfirmationText = document.getElementById("billing-confirmation-text");
    const shippingFields = document.getElementById("shipping-fields-container");
    function toggleBillingFields() {
      if (!billingCheckbox || !billingFields || !billingConfirmationContainer) return;
      if (billingCheckbox.checked) {
        billingFields.style.display = "none";
        billingConfirmationContainer.style.display = "block";
        if (billingConfirmationText) billingConfirmationText.innerHTML = getFormattedShippingAddress();
        copyShippingToBilling();
      } else {
        billingFields.style.display = "block";
        billingConfirmationContainer.style.display = "none";
        if (billingConfirmationText) billingConfirmationText.innerHTML = "";
      }
    }
    function copyShippingToBilling() {
      const fieldsMap = [
        ["id_shipping_first_name", "id_billing_first_name"],
        ["id_shipping_last_name", "id_billing_last_name"],
        ["id_shipping_address_line_1", "id_billing_address_line_1"],
        ["id_shipping_address_line_2", "id_billing_address_line_2"],
        ["id_shipping_city", "id_billing_city"],
        ["id_shipping_county", "id_billing_county"],
        ["id_shipping_postcode", "id_billing_postcode"],
        ["id_shipping_country", "id_billing_country"]
      ];
      fieldsMap.forEach(([shippingId, billingId]) => {
        const shippingField = document.getElementById(shippingId);
        const billingField = document.getElementById(billingId);
        if (shippingField && billingField) {
          billingField.value = shippingField.value;
        }
      });
    }
    if (billingCheckbox && shippingFields) {
      billingCheckbox.addEventListener("change", toggleBillingFields);
      const shippingInputs = shippingFields.querySelectorAll("input, select");
      shippingInputs.forEach((input) => {
        const eventType = input.tagName === "SELECT" ? "change" : "input";
        input.addEventListener(eventType, () => {
          if (billingCheckbox.checked && billingConfirmationText) {
            billingConfirmationText.innerHTML = getFormattedShippingAddress();
          }
        });
      });
      toggleBillingFields();
    }
    document.querySelectorAll(".js-qty-minus").forEach(function(btn) {
      btn.addEventListener("click", function() {
        const input = btn.closest("form").querySelector('input[name="quantity"]');
        if (!input) return;
        const current = parseInt(input.value, 10) || 1;
        if (current > 1) input.value = current - 1;
      });
    });
    document.querySelectorAll(".js-qty-plus").forEach(function(btn) {
      btn.addEventListener("click", function() {
        const input = btn.closest("form").querySelector('input[name="quantity"]');
        if (!input) return;
        const current = parseInt(input.value, 10) || 1;
        const max = parseInt(input.max, 10) || 999;
        if (current < max) input.value = current + 1;
      });
    });
    document.querySelectorAll(".js-cart-item-form").forEach(function(form) {
      form.addEventListener("submit", function(e) {
        e.preventDefault();
        handleCartUpdate(form);
      });
    });
    document.querySelectorAll(".js-remove-item").forEach(function(btn) {
      btn.addEventListener("click", function() {
        const artworkId = btn.dataset.artworkId;
        if (artworkId) handleRemoveItem(artworkId);
      });
    });
    if (placeOrderButton && confirmModal && finalConfirmBtn) {
      placeOrderButton.addEventListener("click", function(e) {
        e.preventDefault();
        e.stopPropagation();
        const validationErrors = validateCheckoutForm();
        if (validationErrors.length > 0) {
          const errorMsg = validationErrors.join("\n");
          if (window.Toast) {
            validationErrors.forEach((err) => window.Toast.show(err, "error", 8e3));
          } else {
            alert(errorMsg);
          }
          return;
        }
        if (billingCheckbox && billingCheckbox.checked) {
          copyShippingToBilling();
        }
        populateConfirmationModal();
        confirmModal.showModal();
      });
      finalConfirmBtn.addEventListener("click", async function(e) {
        e.preventDefault();
        e.stopPropagation();
        if (paymentInProgress) {
          console.warn("Payment already in progress. Please wait.");
          return;
        }
        const modalContent = confirmModal.querySelector(".modal-box");
        if (modalContent) {
          modalContent.scrollTop = 0;
        }
        paymentInProgress = true;
        if (modalLoadingSpinner) modalLoadingSpinner.style.display = "block";
        finalConfirmBtn.disabled = true;
        if (billingCheckbox && billingCheckbox.checked) {
          copyShippingToBilling();
        }
        const formDataObj = Object.fromEntries(new FormData(checkoutForm).entries());
        try {
          if (!card) throw new Error("Payment form not initialized, please refresh the page.");
          const countryVal = getValue("id_billing_country") || getValue("id_shipping_country");
          const isoCountry = countryVal.length ? countryVal.trim().substring(0, 2).toUpperCase() : "GB";
          const phonePrefixInput = document.getElementById("id_phone_0");
          const phoneNumberInput = document.getElementById("id_phone_1");
          const authPhoneInput = document.getElementById("id_phone");
          let fullPhone = "";
          if (phonePrefixInput && phoneNumberInput && phonePrefixInput.offsetParent !== null) {
            const rawPrefix = phonePrefixInput.value;
            const cleanPrefix = rawPrefix.replace(/[^0-9+]/g, "");
            fullPhone = (cleanPrefix + phoneNumberInput.value).trim();
          } else if (authPhoneInput) {
            fullPhone = authPhoneInput.value.replace(/[^0-9+]/g, "").trim();
          } else {
            let rawString = formDataObj["phone"] || formDataObj["id_phone_0"] + formDataObj["id_phone_1"] || "";
            fullPhone = rawString.replace(/[^0-9+]/g, "").trim();
          }
          formDataObj["phone"] = fullPhone;
          console.log("Full Phone:", fullPhone);
          let finalEmail = getValue("id_email") || formDataObj["email"] || "";
          if (!finalEmail) {
            const hiddenEmailInput = document.getElementById("id-email");
            if (hiddenEmailInput) {
              finalEmail = hiddenEmailInput.value;
            }
          }
          const amountClean = finalConfirmBtn.dataset.amount;
          if (!amountClean) throw new Error("Payment amount not found.");
          const amountString = amountClean.replace(/,/g, "");
          const billingContact = {
            givenName: getValue("id_billing_first_name") || getValue("id_shipping_first_name"),
            familyName: getValue("id_billing_last_name") || getValue("id_shipping_last_name"),
            email: finalEmail,
            addressLines: [
              getValue("id_billing_address_line_1") || getValue("id_shipping_address_line_2")
            ],
            city: getValue("id_billing_city") || getValue("id_shipping_city"),
            postalCode: getValue("id_billing_postcode") || getValue("id_shipping_postcode"),
            state: getValue("id_billing_county") || getValue("id_shipping_county"),
            countryCode: isoCountry
          };
          const line2 = getValue("id_billing_address_line_2") || getValue("id_shipping_address_line_2");
          if (line2) {
            billingContact.addressLines.push(line2);
          }
          const stateVal = getValue("id_billing_county") || getValue("id_shipping_county");
          if (stateVal) {
            billingContact.state = stateVal;
          }
          if (fullPhone && fullPhone.length > 5) {
            billingContact.phone = fullPhone;
          }
          console.log("Billing Contact:", billingContact);
          const verificationDetails = {
            amount: amountString,
            billingContact,
            currencyCode: "GBP",
            intent: "CHARGE",
            customerInitiated: true,
            sellerKeyedIn: false
          };
          console.log("Verification Details:", verificationDetails);
          await delay(3e3);
          confirmModal.close();
          if (placeOrderButton) {
            placeOrderButton.innerHTML = '<i class="fa-solid fa-shield-halved fa-spin mr-2"></i> Verifying Security...';
            placeOrderButton.disabled = true;
          }
          const tokenResult = await card.tokenize(verificationDetails);
          if (tokenResult.status !== "OK") {
            const errorMsg = tokenResult.errors?.[0]?.message || "Tokenization failed";
            throw new Error(errorMsg);
          }
          if (placeOrderButton) {
            placeOrderButton.innerHTML = '<i class="fa-solid fa-spinner fa-spin mr-2"></i> Finalizing Order...';
          }
          const response = await fetch("/order/confirmation/", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "X-Requested-With": "XMLHttpRequest",
              "X-CSRFToken": getCsrfToken()
            },
            body: JSON.stringify({
              sourceId: tokenResult.token,
              formData: formDataObj
            }),
            credentials: "include"
          });
          const result = await response.json();
          if (result.status === "success") {
            window.location.href = result.redirect_url;
          } else {
            throw new Error(result.message || "Payment failed");
          }
        } catch (err) {
          console.error("Payment failed:", err);
          if (modalLoadingSpinner) modalLoadingSpinner.style.display = "none";
          finalConfirmBtn.disabled = false;
          paymentInProgress = false;
          if (placeOrderButton) {
            placeOrderButton.disabled = false;
            placeOrderButton.innerHTML = '<i class="fa-solid fa-credit-card mr-2"></i> Confirm & Pay';
          }
          const errorMessage = err.message || "An error occurred during payment processing.";
          if (window.Toast) {
            window.Toast.show(errorMessage, "error");
          } else {
            alert("Error: " + errorMessage);
          }
        }
      });
    }
  });
})();
//# sourceMappingURL=checkout.js.map
(()=>{function M(){let e=document.querySelector("[name=csrfmiddlewaretoken]");return e?e.value:""}async function N(){let e=document.getElementById("cart-dropdown-content");if(!e){console.warn("Cart dropdown element not found. Cannot update.");return}try{let i=await fetch("/checkout/cart-dropdown/",{method:"GET",headers:{"X-Requested-With":"XMLHttpRequest"},credentials:"include"});if(!i.ok)throw new Error(`Failed to fetch cart: ${i.status}`);let o=await i.json();e.innerHTML=o.html}catch(i){console.error("Error refreshing cart dropdown:",i),e.innerHTML='<div class="p-4 text-error">Could not load cart.</div>'}}function R(){let e=document.getElementById("cart-dropdown-content");if(!e)return;let i=e.closest(".dropdown");i&&(i.classList.add("dropdown-open"),setTimeout(()=>{i.classList.remove("dropdown-open")},3e3))}function A(){N()}typeof window<"u"&&(window.cart={init:A,updateCartDropdownHTML:N,openCartDropdown:R});document.addEventListener("DOMContentLoaded",()=>{window.cart&&window.cart.init()});var b=null,D=null,S=!1,W=e=>new Promise(i=>setTimeout(i,e));function j(){let e="#FAFAFA",i="#050505";return{".input-container":{borderColor:"#2563EB",borderRadius:"4px",borderWidth:"1px"},input:{backgroundColor:e,color:i,fontSize:"16px"},"input::placeholder":{color:i},".message-text":{color:"#ef4444"},".message-icon":{color:"#ef4444"}}}async function z(){let e=document.getElementById("square-app-id"),i=document.getElementById("square-location-id");if(!e||!i){console.error("Square Credentials not found in DOM");return}let o=JSON.parse(e.textContent),s=JSON.parse(i.textContent);try{if(!window.Square)throw new Error("Square.js script not loaded");D=window.Square.payments(o,s);let l=j();b=await D.card({style:l}),await b.attach("#card-container")}catch(l){console.error("Error initializing Square Payments:",l),window.Toast&&window.Toast.show("Error initializing payment form.","error")}}function T(e){let i=document.getElementById(e);return i&&i.selectedIndex!==-1?i.options[i.selectedIndex].text:""}function n(e){let i=document.getElementById(e);return i?i.value:""}function X(){let e=[];if(!document.getElementById("checkout-form"))return e.push("Checkout form not found."),e;[{id:"id_shipping_first_name",label:"Shipping First Name"},{id:"id_shipping_last_name",label:"Shipping Last Name"},{id:"id_shipping_address_line_1",label:"Shipping Address"},{id:"id_shipping_city",label:"Shipping City"},{id:"id_shipping_postcode",label:"Shipping Postcode"},{id:"id_shipping_country",label:"Shipping Country"}].forEach(l=>{let t=document.getElementById(l.id);(!t||t.value.trim()==="")&&e.push(`${l.label} is required.`)});let s=document.getElementById("id_billing_same_as_shipping");return s&&!s.checked&&[{id:"id_billing_first_name",label:"Billing First Name"},{id:"id_billing_last_name",label:"Billing Last Name"},{id:"id_billing_address_line_1",label:"Billing Address"},{id:"id_billing_city",label:"Billing City"},{id:"id_billing_postcode",label:"Billing Postcode"},{id:"id_billing_country",label:"Billing Country"}].forEach(t=>{let d=document.getElementById(t.id);(!d||d.value.trim()==="")&&e.push(`${t.label} is required.`)}),e}function V(){let e={firstName:n("id_shipping_first_name"),lastName:n("id_shipping_last_name"),line1:n("id_shipping_address_line_1"),line2:n("id_shipping_address_line_2"),city:n("id_shipping_city"),county:n("id_shipping_county"),postcode:n("id_shipping_postcode"),country:T("id_shipping_country")},i=(c,w)=>{let h=document.getElementById(c);h&&(h.textContent=w)};i("modal-shipping-first-name",e.firstName),i("modal-shipping-last-name",e.lastName),i("modal-shipping-line1",e.line1),i("modal-shipping-city",e.city),i("modal-shipping-postcode",e.postcode),i("modal-shipping-country",e.country);let o=document.getElementById("modal-shipping-line2-wrapper");o&&(o.style.display=e.line2?"block":"none"),e.line2&&i("modal-shipping-line2",e.line2);let s=document.getElementById("modal-shipping-county-wrapper");s&&(s.style.display=e.county?"block":"none"),e.county&&i("modal-shipping-county",e.county);let l=document.getElementById("id_billing_same_as_shipping"),t;l&&l.checked?t={...e}:t={firstName:n("id_billing_first_name"),lastName:n("id_billing_last_name"),line1:n("id_billing_address_line_1"),line2:n("id_billing_address_line_2"),city:n("id_billing_city"),county:n("id_billing_county"),postcode:n("id_billing_postcode"),country:T("id_billing_country")},i("modal-billing-first-name",t.firstName),i("modal-billing-last-name",t.lastName),i("modal-billing-line1",t.line1),i("modal-billing-city",t.city),i("modal-billing-postcode",t.postcode),i("modal-billing-country",t.country);let d=document.getElementById("modal-billing-line2-wrapper");d&&(d.style.display=t.line2?"block":"none"),t.line2&&i("modal-billing-line2",t.line2);let r=document.getElementById("modal-billing-county-wrapper");r&&(r.style.display=t.county?"block":"none"),t.county&&i("modal-billing-county",t.county)}function H(){let e=[],i=n("id_shipping_first_name"),o=n("id_shipping_last_name"),s=n("id_shipping_address_line_1"),l=n("id_shipping_address_line_2"),t=n("id_shipping_city"),d=n("id_shipping_county"),r=n("id_shipping_postcode"),c=T("id_shipping_country");return(i||o)&&e.push(i+" "+o),s&&e.push(s),l&&e.push(l),t&&e.push(t),d&&e.push(d),r&&e.push(r),c&&e.push(c),e.join("<br>")}document.addEventListener("DOMContentLoaded",async function(){await z();let e=document.getElementById("place-order-button"),i=document.getElementById("confirm-order-modal"),o=document.getElementById("modal-confirm-btn"),s=document.getElementById("modal-loading-spinner"),l=document.getElementById("checkout-form"),t=document.getElementById("billing-fields-container"),d=document.querySelector(".billing-confirmation-container"),r=document.getElementById("id_billing_same_as_shipping"),c=document.getElementById("billing-confirmation-text"),w=document.getElementById("shipping-fields-container");function h(){!r||!t||!d||(r.checked?(t.style.display="none",d.style.display="block",c&&(c.innerHTML=H()),E()):(t.style.display="block",d.style.display="none",c&&(c.innerHTML="")))}function E(){[["id_shipping_first_name","id_billing_first_name"],["id_shipping_last_name","id_billing_last_name"],["id_shipping_address_line_1","id_billing_address_line_1"],["id_shipping_address_line_2","id_billing_address_line_2"],["id_shipping_city","id_billing_city"],["id_shipping_county","id_billing_county"],["id_shipping_postcode","id_billing_postcode"],["id_shipping_country","id_billing_country"]].forEach(([p,a])=>{let u=document.getElementById(p),_=document.getElementById(a);u&&_&&(_.value=u.value)})}r&&w&&(r.addEventListener("change",h),w.querySelectorAll("input, select").forEach(p=>{let a=p.tagName==="SELECT"?"change":"input";p.addEventListener(a,()=>{r.checked&&c&&(c.innerHTML=H())})}),h()),e&&i&&o&&(e.addEventListener("click",function(m){m.preventDefault(),m.stopPropagation();let p=X();if(p.length>0){let a=p.join(`
`);window.Toast?p.forEach(u=>window.Toast.show(u,"error",8e3)):alert(a);return}r&&r.checked&&E(),V(),i.showModal()}),o.addEventListener("click",async function(m){if(m.preventDefault(),m.stopPropagation(),S){console.warn("Payment already in progress. Please wait.");return}let p=i.querySelector(".modal-box");p&&(p.scrollTop=0),S=!0,s&&(s.style.display="block"),o.disabled=!0,r&&r.checked&&E();let a=Object.fromEntries(new FormData(l).entries());try{if(!b)throw new Error("Payment form not initialized, please refresh the page.");let u=n("id_billing_country")||n("id_shipping_country"),_=u.length?u.trim().substring(0,2).toUpperCase():"GB",C=document.getElementById("id_phone_0"),L=document.getElementById("id_phone_1"),v=document.getElementById("id_phone"),g="";C&&L&&C.offsetParent!==null?g=(C.value.replace(/[^0-9+]/g,"")+L.value).trim():v?g=v.value.replace(/[^0-9+]/g,"").trim():g=(a.phone||a.id_phone_0+a.id_phone_1||"").replace(/[^0-9+]/g,"").trim(),a.phone=g,console.log("Full Phone:",g);let B=n("id_email")||a.email||"";if(!B){let f=document.getElementById("id-email");f&&(B=f.value)}let F=o.dataset.amount;if(!F)throw new Error("Payment amount not found.");let O=F.replace(/,/g,""),y={givenName:n("id_billing_first_name")||n("id_shipping_first_name"),familyName:n("id_billing_last_name")||n("id_shipping_last_name"),email:B,addressLines:[n("id_billing_address_line_1")||n("id_shipping_address_line_2")],city:n("id_billing_city")||n("id_shipping_city"),postalCode:n("id_billing_postcode")||n("id_shipping_postcode"),state:n("id_billing_county")||n("id_shipping_county"),countryCode:_},q=n("id_billing_address_line_2")||n("id_shipping_address_line_2");q&&y.addressLines.push(q);let x=n("id_billing_county")||n("id_shipping_county");x&&(y.state=x),g&&g.length>5&&(y.phone=g),console.log("Billing Contact:",y);let P={amount:O,billingContact:y,currencyCode:"GBP",intent:"CHARGE",customerInitiated:!0,sellerKeyedIn:!1};console.log("Verification Details:",P),await W(3e3),i.close(),e&&(e.innerHTML='<i class="fa-solid fa-shield-halved fa-spin mr-2"></i> Verifying Security...',e.disabled=!0);let I=await b.tokenize(P);if(I.status!=="OK"){let f=I.errors?.[0]?.message||"Tokenization failed";throw new Error(f)}e&&(e.innerHTML='<i class="fa-solid fa-spinner fa-spin mr-2"></i> Finalizing Order...');let k=await(await fetch("/order/confirmation/",{method:"POST",headers:{"Content-Type":"application/json","X-Requested-With":"XMLHttpRequest","X-CSRFToken":M()},body:JSON.stringify({sourceId:I.token,formData:a}),credentials:"include"})).json();if(k.status==="success")window.location.href=k.redirect_url;else throw new Error(k.message||"Payment failed")}catch(u){console.error("Payment failed:",u),s&&(s.style.display="none"),o.disabled=!1,S=!1,e&&(e.disabled=!1,e.innerHTML='<i class="fa-solid fa-credit-card mr-2"></i> Confirm & Pay');let _=u.message||"An error occurred during payment processing.";window.Toast?window.Toast.show(_,"error"):alert("Error: "+_)}}))});})();
