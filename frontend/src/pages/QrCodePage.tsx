import { useState } from "react";
import {
  Container,
  Stack,
  Title,
  NumberInput,
  Button,
} from "@mantine/core";
import { api } from "../apiClient";

export default function QrCodePage() {
  const [amount, setAmount] = useState<number | string>(1);
  const [loading, setLoading] = useState(false);

  async function printQrCodes() {
    if (typeof amount !== "number" || amount < 1) return;

    setLoading(true);

    try {
      await api.post("qrcode", {
        "amount": amount
      });

    } finally {
      setLoading(false);
    }
  }

  return (
    <Container size="xs" py="xl">
      <Stack>
        <Title>Aantal QR-codes</Title>

        <NumberInput
          label="Hoeveel QR-codes wil je afdrukken?"
          min={1}
          value={amount}
          onChange={setAmount}
        />

        <Button loading={loading} onClick={printQrCodes}>
          Afdrukken
        </Button>
      </Stack>
    </Container>
  );
}