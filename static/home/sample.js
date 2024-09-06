document.addEventListener('DOMContentLoaded', function() {

    const content = document.getElementById('content');

    const dashboardBtn = document.getElementById('dashboardBtn');
    const visaRequirementBtn = document.getElementById('visaRequirementBtn');
    const aiConsultantBtn = document.getElementById('aiConsultantBtn');

    const notificationsBtn = document.getElementById('notificationsBtn');
    const settingsBtn = document.getElementById('settingsBtn');
    const supportBtn = document.getElementById('supportBtn');
    const profileBtn = document.getElementById('profileBtn');

    const dashboardMacro = document.getElementById('dashboardMacro')

    window.functionDashboard = function() {
        content.innerHTML = "";
        dashboardMacro.style.display = "block";
        content.appendChild(dashboardMacro);

        dashboardBtn.classList.add('selected');
        visaRequirementBtn.classList.remove('selected');
        aiConsultantBtn.classList.remove('selected');
        notificationsBtn.classList.remove('selected');
        settingsBtn.classList.remove('selected');
        supportBtn.classList.remove('selected');
        profileBtn.classList.remove('selected');
    };

    const visaRequirementMacro = document.getElementById('visaRequirementMacro')

    window.functionVisaRequirement = function() {
        content.innerHTML = "";
        visaRequirementMacro.style.display = "block";
        content.appendChild(visaRequirementMacro);

        visaRequirementBtn.classList.add('selected');
        dashboardBtn.classList.remove('selected');
        aiConsultantBtn.classList.remove('selected');
        notificationsBtn.classList.remove('selected');
        settingsBtn.classList.remove('selected');
        supportBtn.classList.remove('selected');
        profileBtn.classList.remove('selected');
    }

    const visaProGPTMacro = document.getElementById('visaProGPTMacro')

    window.functionAIConsultant = function() {
        content.innerHTML = "";
        visaProGPTMacro.style.display = "block";
        content.appendChild(visaProGPTMacro);

        aiConsultantBtn.classList.add('selected');
        visaRequirementBtn.classList.remove('selected');
        dashboardBtn.classList.remove('selected');
        notificationsBtn.classList.remove('selected');
        settingsBtn.classList.remove('selected');
        supportBtn.classList.remove('selected');
        profileBtn.classList.remove('selected');
    };

    const notificationsMacro = document.getElementById('notificationsMacro')

    window.functionNotifications = function() {
        content.innerHTML = "";
        notificationsMacro.style.display = "block";
        content.appendChild(notificationsMacro);

        notificationsBtn.classList.add('selected');
        dashboardBtn.classList.remove('selected');
        visaRequirementBtn.classList.remove('selected');
        aiConsultantBtn.classList.remove('selected');
        settingsBtn.classList.remove('selected');
        supportBtn.classList.remove('selected');
        profileBtn.classList.remove('selected');
    };

    const settingsMacro = document.getElementById('settingsMacro')

    window.functionSettings = function() {
        content.innerHTML = "";
        settingsMacro.style.display = "block";
        content.appendChild(settingsMacro);

        settingsBtn.classList.add('selected');
        dashboardBtn.classList.remove('selected');
        visaRequirementBtn.classList.remove('selected');
        aiConsultantBtn.classList.remove('selected');
        notificationsBtn.classList.remove('selected');
        supportBtn.classList.remove('selected');
        profileBtn.classList.remove('selected');
    };

    const supportMacro = document.getElementById('supportMacro')

    window.functionSupport = function() {
        content.innerHTML = "";
        supportMacro.style.display = "block";
        content.appendChild(supportMacro);

        supportBtn.classList.add('selected');
        dashboardBtn.classList.remove('selected');
        visaRequirementBtn.classList.remove('selected');
        aiConsultantBtn.classList.remove('selected');
        notificationsBtn.classList.remove('selected');
        settingsBtn.classList.remove('selected');
        profileBtn.classList.remove('selected');
    };

    const profileMacro = document.getElementById('profileMacro')

    window.functionProfile = function() {
        content.innerHTML = "";
        profileMacro.style.display = "block";
        content.appendChild(profileMacro);

        profileBtn.classList.add('selected');
        dashboardBtn.classList.remove('selected');
        visaRequirementBtn.classList.remove('selected');
        aiConsultantBtn.classList.remove('selected');
        notificationsBtn.classList.remove('selected');
        settingsBtn.classList.remove('selected');
        supportBtn.classList.remove('selected');
    };

});