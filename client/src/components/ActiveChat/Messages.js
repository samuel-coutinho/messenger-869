import React from "react";
import { Box } from "@material-ui/core";
import { SenderBubble, OtherUserBubble } from "../ActiveChat";
import moment from "moment";

const Messages = (props) => {
  const { messages, otherUser, user, lastReadMessageId } = props;

  return (
    <Box>
      {messages.map((message) => {
        const time = moment(message.createdAt).format("MMM Do YY, h:mm:ss a");
        const isLastReadMessageId = lastReadMessageId === message.id ? true : false;        

        return message.senderId === user.id ? (
          <SenderBubble
            key={message.id}
            text={message.text}
            time={time}
            otherUser={otherUser}
            isLastReadMessageId={isLastReadMessageId}
          />
        ) : (
          <OtherUserBubble
            key={message.id}
            text={message.text}
            time={time}
            otherUser={otherUser}
          />
        );
      })}
    </Box>
  );
};

export default Messages;
