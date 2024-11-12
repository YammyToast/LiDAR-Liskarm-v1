      // ==================================
      // SHARED

      const shared = {
        nav_window_state: -1,
      };

      const KEYBINDS = {
        ROBOT_FORWARDS: "W",
        ROBOT_BACKWARDS: "S",
        ROBOT_TURN_LEFT: "A",
        ROBOT_TURN_RIGHT: "D",
        CAMERA_FULL_SCREEN: "F",
        CAMERA_COLOUR: "R",
        CAMERA_LIDAR: "T",
      };

      const CAMERA_AUXILIARY = new Map([
        ["Fullscreen", KEYBINDS.CAMERA_FULL_SCREEN],
        ["Colour", KEYBINDS.CAMERA_COLOUR],
        ["LIDAR", KEYBINDS.CAMERA_LIDAR],
      ]);

      const CAMERA_CONTROLS = new Map([
        ["Forwards", KEYBINDS.ROBOT_FORWARDS],
        ["Backwards", KEYBINDS.ROBOT_BACKWARDS],
        ["Turn Left", KEYBINDS.ROBOT_TURN_LEFT],
        ["Turn Right", KEYBINDS.ROBOT_TURN_RIGHT],
      ]);

      function make_keyboard_icon(__k) {
        let key_icon = document.createElement("div");
        key_icon.className = "keyboard-btn-icon";
        key_icon.textContent = __k;
        return key_icon;
      }

      // ==================================
      // DISPLAY FUNCTIONS
      function display_overview() {
        console.log("Nothing to do for overview...");
      }

      const DISPLAY_FUNCTIONS = new Map([[1, display_overview], [2], [3], [4]]);
      const DISPLAY_ELEMENTS = new Map([
        [1, document.getElementById("display-overview")],
        [2, document.getElementById("display-camera")],
      ]);

      function change_display(__new_active) {
        shared.nav_window_state = __new_active;
        try {
          // hide all and display active
          hide_all_displays();
          DISPLAY_ELEMENTS.get(__new_active).classList.remove("hidden");
          DISPLAY_FUNCTIONS.get(__new_active)();
        } catch (error) {
          console.error(`Unbound display pointer: ${__new_active}`);
        }
      }

      function hide_all_displays() {
        DISPLAY_ELEMENTS.forEach((element, k) => {
          element.classList.add("hidden");
        });
      }

      // Initialize all the menus as hidden.
      hide_all_displays();

      // ==================================
      // NAV BUTTONS
      let nav_btn_style_active =
        "flex h-fit w-100 items-center px-4 py-2 text-lg border-2 border-s-text-color hover:border-accent-2 cursor-pointer duration-200";
      let nav_btn_style_inactive =
        "flex h-fit w-100 items-center px-4 py-2 text-lg border-2 border-b-background border-accent-1 hover:border-accent-2 cursor-pointer duration-200";

      const NAV_BTN_MAP = new Map([
        [1, document.getElementById("nav-btn-overview")],
        [2, document.getElementById("nav-btn-camera")],
        [3, document.getElementById("nav-btn-actionsheet")],
        [4, document.getElementById("nav-btn-log")],
      ]);

      function handle_nav_btn(__new_active) {
        NAV_BTN_MAP.forEach((btn, k) => {
          btn.className = nav_btn_style_inactive;
        });
        NAV_BTN_MAP.get(__new_active).className = nav_btn_style_active;
        // Update the display with the new
        change_display(__new_active);
      }

      NAV_BTN_MAP.forEach((btn, k) => {
        // Bind nav buttons to function
        btn.addEventListener("click", () => {
          handle_nav_btn(k);
        });
        // Create key bind icons
        btn.prepend(make_keyboard_icon(k));
      });

      document.addEventListener("keydown", (e) => {
        let int_parse = parseInt(e.key);
        if (NAV_BTN_MAP.has(int_parse)) {
          handle_nav_btn(int_parse);
        }
      });

      // Set initial window state and thus button
      shared.nav_window_state = 2;
      handle_nav_btn(shared.nav_window_state);

      // ==================================
      // CAMERA BUTTONS
      let camera_bar_auxiliary = document.getElementById(
        "camera-bar-auxiliary"
      );

      let camera_bar_controls = document.getElementById(
        "camera-bar-controls"
      );

      function make_keybind_containers(__k, __description) {
        let container = document.createElement("div");
        container.className = "camera-keybind-container";
        container.textContent = __description;
        container.prepend(make_keyboard_icon(__k));
        return container;
      }

      CAMERA_AUXILIARY.forEach((k, description) => {
        camera_bar_auxiliary.append(
          make_keybind_containers(k, description)
        );
      });

      CAMERA_CONTROLS.forEach((k, description) => {
        camera_bar_controls.append(
          make_keybind_containers(k, description)
        );
      });