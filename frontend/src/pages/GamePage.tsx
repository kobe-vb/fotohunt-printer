import { Container, Title, Text } from '@mantine/core';

export default function GamePage() {

  return (
    <Container size="sm" py="xl">
      <Title>Game</Title>
      <Text>Team ID: {teamId}</Text>
    </Container>
  );
}