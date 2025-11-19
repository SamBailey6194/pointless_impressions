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
          console.log("Raw Country Value:", countryVal);
          const isoCountry = countryVal.length ? countryVal.trim().substring(0, 2).toUpperCase() : "GB";
          const phonePrefixInput = document.getElementById("id_phone_0");
          const phoneNumberInput = document.getElementById("id_phone_1");
          const authUserPhone = document.getElementById("id_phone");
          let fullPhone = "";
          if (phonePrefixInput && phoneNumberInput && phonePrefixInput.offsetParent !== null) {
            const rawPrefix = phonePrefixInput.value;
            const cleanPrefix = rawPrefix.replace(/[^0-9+]/g, "");
            fullPhone = (cleanPrefix + phoneNumberInput.value).trim();
          } else if (authUserPhone) {
            fullPhone = authUserPhone.value.replace(/[^0-9+]/g, "").trim();
          } else {
            let rawString = formDataObj["phone"] || formDataObj["id_phone_0"] + formDataObj["id_phone_1"] || "";
            fullPhone = rawString.replace(/[^0-9+]/g, "").trim();
          }
          const amountString = finalConfirmBtn.dataset.amount;
          if (!amountString) throw new Error("Payment amount not found.");
          const verificationDetails = {
            amount: amountString,
            billingContact: {
              givenName: getValue("id_billing_first_name") || getValue("id_shipping_first_name"),
              familyName: getValue("id_billing_last_name") || getValue("id_shipping_last_name"),
              email: getValue("id_email") || formDataObj["email"],
              phone: fullPhone,
              addressLines: [
                getValue("id_billing_address_line_1") || getValue("id_shipping_address_line_2"),
                getValue("id_billing_address_line_2") || getValue("id_shipping_address_line_2")
              ],
              city: getValue("id_billing_city") || getValue("id_shipping_city"),
              postalCode: getValue("id_billing_postcode") || getValue("id_shipping_postcode"),
              state: getValue("id_billing_county") || getValue("id_shipping_county"),
              countryCode: isoCountry
            },
            currencyCode: "GBP",
            intent: "CHARGE",
            customerInitiated: true,
            sellerKeyedIn: false
          };
          setTimeout(() => {
            confirmModal.close();
          }, 3e3);
          if (placeOrderButton) {
            placeOrderButton.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Processing...';
            placeOrderButton.disabled = true;
          }
          const tokenResult = await card.tokenize(verificationDetails);
          if (tokenResult.status !== "OK") {
            const errorMsg = tokenResult.errors?.[0]?.message || "Tokenization failed";
            throw new Error(errorMsg);
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
            placeOrderButton.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Processing...';
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
