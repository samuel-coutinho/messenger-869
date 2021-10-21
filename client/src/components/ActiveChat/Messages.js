import React from "react";
import { Box } from "@material-ui/core";
import { SenderBubble, OtherUserBubble } from "../ActiveChat";
import  moment  from "moment";

const Messages = (props) => {
  const { messages, otherUser, userId } = props;
  
  const sortedMessagesByCreatedAt = messages.slice().sort((a, b) => moment(a.createdAt) - moment(b.createdAt));

  return (
    <Box>
      { sortedMessagesByCreatedAt.map((message) => {
        const time = moment(message.createdAt).format('MMM Do YY, h:mm:ss a');

        return message.senderId === userId ? (
          <SenderBubble key={message.id} text={message.text} time={time} />
        ) : (
          <OtherUserBubble key={message.id} text={message.text} time={time} otherUser={otherUser} />
        );
      })}
    </Box>
  );
};

export default Messages;