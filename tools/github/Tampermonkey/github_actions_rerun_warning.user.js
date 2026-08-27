// ==UserScript==
// @name         GitHub Actions Re-run Warning & Fresh Trigger
// @namespace    https://github.com/sl5net
// @version      1.2
// @description  Warn on old re-runs and add fresh workflow trigger button
// @match        https://github.com/*
// @grant        none
// ==/UserScript==

(function () {
    'use strict';

    function applyWarningStyles(element) {
        element.style.backgroundColor = '#fff3cd';
        element.style.borderColor = '#ffeeba';
        element.style.color = '#856404';
    }

    function getWorkflowUrl() {
        const workflowLink = document.querySelector('a[href*="/actions/workflows/"]');
        if (workflowLink) {
            return workflowLink.href;
        }
        const pathParts = window.location.pathname.split('/');
        if (pathParts.length >= 3) {
            return `/${pathParts[1]}/${pathParts[2]}/actions`;
        }
        return null;
    }

    function injectFreshButton(parentButton) {
        if (document.getElementById('fresh-workflow-trigger-btn')) {
            return;
        }

        const freshBtn = document.createElement('a');
        freshBtn.id = 'fresh-workflow-trigger-btn';
        freshBtn.className = 'Button--primary Button--medium Button';
        freshBtn.textContent = 'Run this Workflow (Fresh)';
        freshBtn.style.marginLeft = '8px';
        freshBtn.style.backgroundColor = '#238636';
        freshBtn.style.color = '#ffffff';
        freshBtn.style.display = 'inline-flex';
        freshBtn.style.alignItems = 'center';
        freshBtn.style.textDecoration = 'none';
        freshBtn.style.fontWeight = 'bold';
        freshBtn.style.padding = '5px 12px';
        freshBtn.style.borderRadius = '6px';

        const targetUrl = getWorkflowUrl();
        if (targetUrl) {
            freshBtn.href = targetUrl;
        }

        const container = parentButton.parentElement;
        if (container) {
            container.appendChild(freshBtn);
        }
    }

    function updateUi() {
        const labels = document.querySelectorAll('.Button-label, [role="menuitem"], [role="menuitem"] span, button');
        labels.forEach((el) => {
            if (el.children.length > 0 && !el.classList.contains('Button-label') && el.getAttribute('role') !== 'menuitem') {
                return;
            }
            const text = el.textContent.trim();
            if (text.startsWith('Re-run') && !text.includes('⚠️')) {
                if (text.includes('failed jobs')) {
                    el.textContent = 'Re-run failed jobs ⚠️ NOT the failed Workflow!!';
                } else if (text === 'Re-run jobs') {
                    el.textContent = 'Re-run jobs ⚠️ NOT the failed Workflow!!';
                } else if (text.includes('all jobs')) {
                    el.textContent = 'Re-run all jobs ⚠️ (Old commit only!)';
                }

                const buttonParent = el.closest('button, [role="menuitem"]');
                if (buttonParent) {
                    applyWarningStyles(buttonParent);
                    if (buttonParent.tagName.toLowerCase() === 'button') {
                        injectFreshButton(buttonParent);
                    }
                }
            }
        });
    }

    const observer = new MutationObserver(updateUi);
    observer.observe(document.body, { childList: true, subtree: true });
    updateUi();
})();


