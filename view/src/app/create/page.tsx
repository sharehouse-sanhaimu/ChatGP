"use client";

import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";
import Image from "next/image";
import { useRouter } from "next/navigation";
import { Card } from "@/components/ui/card";
import { useForm, SubmitHandler } from "react-hook-form";
import { useState } from "react";

type Input = {
  text: string;
};

export default function Home() {
  const router = useRouter();
  const [submit, setSubmit] = useState<boolean>(false);

  const apiId = process.env.NEXT_PUBLIC_API_ACCESS_ID;
  const apiKey = process.env.NEXT_PUBLIC_API_ACCESS_KEY;
  const apiUrl = process.env.NEXT_PUBLIC_API_URL;

  if (!apiId || !apiKey || !apiUrl) {
    return (
      <div>
        <h1>環境変数がありません</h1>
      </div>
    );
  }

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<Input>({
    defaultValues: {
      text: "例：宇宙船に乗ってる猫",
    },
  });

  const toBlob = async (base64: string) => {
    try {
      const bin = atob(base64);
      const buffer = new Uint8Array(bin.length).map((_, i) =>
        bin.charCodeAt(i)
      );
      const blob = new Blob([buffer], { type: "image/png" });
      return blob;
    } catch (e) {
      console.error(e);
      return false;
    }
  };

  const onSubmit: SubmitHandler<Input> = async (data: Input) => {
    try {
      setSubmit(true);
      const response = await fetch(`${apiUrl}/1/car/data?text=${data.text}`, {
        headers: {
          [apiId]: apiKey,
        },
      });
      const responseJson = await response.json();
      const dataBase64 = await responseJson.car_img;
      const blob = await toBlob(dataBase64);
      if (blob) {
        const url = URL.createObjectURL(blob);
        localStorage.setItem("UserCar", url);
        router.push("/create/result");
      }
    } catch (error) {
      console.error("Error:", error);
    }
  };
  return (
    <main>
      {submit && (
        <div className="flex flex-col items-center bg-basecolor absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 border-4 border-accentcolor rounded-xl">
          <Image
            src="/loading.png"
            alt="loading"
            width={196}
            height={196}
            priority
            className="animate-spin"
          />
          <div className=" flex flex-col items-center bg-primarycolor text-xl text-basecolor p-4 rounded-md ">
            <p>ChatGPTの生成は時間がかかります！</p>
            <p>少々お待ちください。</p>
          </div>
        </div>
      )}
      <div className="flex flex-wrap justify-around items-center h-screen bg-basecolor">
        <div className="h-4/5 w-1/2 p-4">
          <div className="flex flex-col justify-around items-center h-full w-full bg-primarycolor rounded-xl">
            <Image
              src="/announcer.webp"
              alt="announcer"
              width={256}
              height={256}
              priority
              className=" rounded-sm border-4 border-accentcolor"
            />
            <Card className="text-2xl text-center w-11/12 border-4 border-basecolor p-8">
              <p>これからレースだ！ 君の車を作製しよう！</p>
            </Card>
          </div>
        </div>
        <div className="flex h-4/5 w-1/2 p-4 flex-col justify-around items-center">
          <div className="text-2xl text-center w-11/12 p-4 items-center bg-secondarycolor text-basecolor rounded-md">
            <div className=" p-4">
              <p>これからChatGPに出場する車を</p>
              <p>ChatGPTに作成してもらおう！</p>
            </div>
            <p>車の画像、音、ステータスが君の言葉で決まるよ！</p>
          </div>
          <Card className="w-full p-4 bg-primarycolor">
            <form className="w-full" onSubmit={handleSubmit(onSubmit)}>
              <div className="p-1">
                <div className="text-2xl bg-accentcolor text-basecolor inline-block p-2 rounded-xl">
                  入力欄
                </div>
              </div>
              <Textarea
                className="text-2xl text-center w-full border-4 border-accentcolor"
                {...register("text", { required: true, maxLength: 20 })}
              ></Textarea>
              <div className="flex p-4 justify-end">
                <Button className=" bg-accentcolor hover:bg-secondarycolor text-basecolor w-24 h-12 text-xl text-center">
                  送信
                </Button>
              </div>
              {errors.text && (
                <div className=" bg-basecolor border-secondarycolor border-4 text-2xl text-center text-accentcolor font-bold p-2">
                  20文字以内で入力してください
                </div>
              )}
            </form>
          </Card>
        </div>
      </div>
    </main>
  );
}