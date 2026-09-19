class HolidayTimeMoreInfo extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: "open" });
    this.shadowRoot.innerHTML = `
      <style>
        :host {
          display: block;
          color: var(--primary-text-color);
          font-family: var(--paper-font-body1_-_font-family, inherit);
        }

        .home-date {
          display: grid;
          justify-items: center;
          gap: 6px;
          padding: 12px 24px 28px;
          text-align: center;
        }

        .label {
          color: var(--secondary-text-color);
          font-size: 13px;
          line-height: 1.4;
        }

        .value {
          font-size: clamp(20px, 5vw, 24px);
          font-weight: 500;
          line-height: 1.3;
        }
      </style>
      <more-info-content></more-info-content>
      <div class="home-date" aria-live="polite">
        <span class="label"></span>
        <span class="value"></span>
      </div>
    `;

    this._control = this.shadowRoot.querySelector("more-info-content");
    this._label = this.shadowRoot.querySelector(".label");
    this._value = this.shadowRoot.querySelector(".value");
  }

  set hass(value) {
    this._hass = value;
    this._update();
  }

  set stateObj(value) {
    this._stateObj = value;
    this._update();
  }

  set entry(value) {
    this._entry = value;
    this._update();
  }

  set editMode(value) {
    this._editMode = value;
    this._update();
  }

  set data(value) {
    this._data = value;
    this._update();
  }

  _update() {
    if (!this._stateObj) {
      return;
    }

    // Let HA load its native time control, without recursively selecting us.
    // Clone attributes so the real entity keeps its custom more-info metadata.
    const attributes = { ...this._stateObj.attributes };
    delete attributes.custom_ui_more_info;
    this._control.hass = this._hass;
    this._control.stateObj = { ...this._stateObj, attributes };
    this._control.entry = this._entry;
    this._control.editMode = this._editMode;
    this._control.data = this._data;

    const language = this._hass?.locale?.language ?? navigator.language;
    const norwegian = /^(nb|nn|no)(-|$)/i.test(language);
    const localizedLabel = this._hass?.formatEntityAttributeName?.(
      this._stateObj,
      "homeDate"
    );
    const genericLabels = new Set(["homeDate", "Home date"]);
    this._label.textContent =
      localizedLabel && !genericLabels.has(localizedLabel)
        ? localizedLabel
        : norwegian
          ? "Dato for hjemkomst"
          : "Home date";

    const value = this._stateObj.attributes?.homeDate;
    const date = new Date(value);
    if (!value || Number.isNaN(date.getTime())) {
      this._value.textContent = "—";
      return;
    }

    const options = {
      weekday: "long",
      day: "numeric",
      month: "long",
      year: "numeric",
    };
    if (this._hass?.config?.time_zone) {
      options.timeZone = this._hass.config.time_zone;
    }

    this._value.textContent = new Intl.DateTimeFormat(
      language,
      options
    ).format(date);
  }
}

if (!customElements.get("holiday-time-more-info")) {
  customElements.define("holiday-time-more-info", HolidayTimeMoreInfo);
}
