/* @odoo-module */

import { useComponent, useState } from "@odoo/owl";
import { _t } from "@web/core/l10n/translation";
import { download } from "@web/core/network/download";
import { registry } from "@web/core/registry";
import { patch } from "@web/core/utils/patch";
//import { MessageReactionButton } from "./message_reaction_button";
import { ChatWindowService } from "@mail/core/common/chat_window_service";

const { DateTime } = luxon;

export const messageActionsRegistry = registry.category("mail.message/actions");

const replyToAction = messageActionsRegistry.get("reply-to");
patch(replyToAction, {
    onClick: (component) => {
        console.log("clicked")
        console.log(component)
        console.log(component.threadService)
//        component.threadService.openChat({ 2 })
    },
});

//messageActionsRegistry
//    .add("thread-reply", {
//        condition: (component) => component.canReplyTo,
//        icon: "fa-chat",
//        title: _t("Thread"),
//        onClick: (component) => { console.log('you clicked on thread')},
//        sequence: 15,
//    })


