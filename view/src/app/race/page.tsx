"use client";

import { useState, useEffect } from "react";
import { Interactive } from "./Interactive";
import { Progress } from "./Progress";
import { useRouter } from "next/navigation";
import { SubmitProps, InteProps, ResponceProps, ProgProps } from "./type";
import { RaceData } from "@/app/race/type";
import { getRaceDataFromGpt, getEndDataFromGpt } from "@/lib/race/action";
import {
  PLAYER_CAR,
  PLAYER_CAR_IMAGE,
  PLAYER_CAR_NAME,
  PLAYER_CAR_LUCK,
  PLAYER_CAR_INSTRUCTION,
  PLAYER_CAR_FORTUNE,
  RACE_EVENT,
  RACE_RESPONSE_DATA,
} from "@/lib/const";
import { PlayerCarRes } from "@/app/create/type";

export default function Home() {
  // Sample RaceData
  const sampleRaceData: RaceData = {
    first_car_name: "string",
    second_car_name: "string",
    third_car_name: "string",
    fourth_car_name: "string",
    player_car_name: "string",
    first_car_instruction: "string",
    second_car_instruction: "string",
    third_car_instruction: "string",
    fourth_car_instruction: "string",
    event: "event",
  };

  const testGetRaceInfoFromGpt = async (event: string) => {
    // Sample RaceData
    console.log("sampleRaceData", JSON.stringify(sampleRaceData));
    const responseJson = await getRaceDataFromGpt(sampleRaceData);
    console.log("responseJson:", responseJson);
    return true;
  };

  const router = useRouter();
  // 場面を切り替えるためのState
  const [scene, setScene] = useState<number>(0);
  // InteractiveとProgressを切り替えるState
  const [response, setResponse] = useState<boolean>(false);

  async function onSubmit(data: SubmitProps) {
    if (scene + 1 >= 3) {
      console.log("scene + 1 >= 3");
      const previousResponce = localStorage.getItem(RACE_RESPONSE_DATA);
      if (previousResponce) {
        const previousJson = JSON.parse(previousResponce) as RaceData;
        const sendJson = {
          ...previousJson,
          [RACE_EVENT]: data.event,
        };
        // const responseJson = await getEndDataFromGpt(sendJson);
        // localStorage.setItem(RACE_RESPONSE_DATA, JSON.stringify(responseJson));
        router.push("/race/ending");
      }
    } else {
      console.log("router.push()");
      const previousResponce = localStorage.getItem(RACE_RESPONSE_DATA);
      if (previousResponce) {
        console.log(previousResponce, "previousResponce");
        const previousJson = JSON.parse(previousResponce) as RaceData;
        const sendJson = {
          ...previousJson,
          [RACE_EVENT]: data.event,
        };
        const responseJson = await getRaceDataFromGpt(sendJson);
        if (!responseJson) return <div>Error</div>;
        localStorage.setItem(RACE_RESPONSE_DATA, JSON.stringify(responseJson));
        setResponse(true);
      }
    }
  }

  function nextScene(): void {
    setScene(scene + 1);
    setResponse(false);
  }

  console.log(response, "response");
  if (!response) {
    return (
      <main>
        <Interactive order={1} scene={scene} submit={onSubmit} />
      </main>
    );
  } else
    return (
      <main>
        <Progress order={1} scene={scene} click={nextScene} />
      </main>
    );
}
