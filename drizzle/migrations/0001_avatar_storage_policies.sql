-- Private avatar storage: owners only, folder-per-user

create policy "Owners upload avatar photos"
  on storage.objects for insert to authenticated
  with check (bucket_id = 'avatar-photos' and (storage.foldername(name))[1] = auth.uid()::text);

create policy "Owners read their avatar photos"
  on storage.objects for select to authenticated
  using (bucket_id = 'avatar-photos' and (storage.foldername(name))[1] = auth.uid()::text);

create policy "Owners update their avatar photos"
  on storage.objects for update to authenticated
  using (bucket_id = 'avatar-photos' and (storage.foldername(name))[1] = auth.uid()::text)
  with check (bucket_id = 'avatar-photos' and (storage.foldername(name))[1] = auth.uid()::text);

create policy "Owners delete their avatar photos"
  on storage.objects for delete to authenticated
  using (bucket_id = 'avatar-photos' and (storage.foldername(name))[1] = auth.uid()::text);

create policy "Owners upload avatar assets"
  on storage.objects for insert to authenticated
  with check (bucket_id = 'avatar-assets' and (storage.foldername(name))[1] = auth.uid()::text);

create policy "Owners read their avatar assets"
  on storage.objects for select to authenticated
  using (bucket_id = 'avatar-assets' and (storage.foldername(name))[1] = auth.uid()::text);

create policy "Owners update their avatar assets"
  on storage.objects for update to authenticated
  using (bucket_id = 'avatar-assets' and (storage.foldername(name))[1] = auth.uid()::text)
  with check (bucket_id = 'avatar-assets' and (storage.foldername(name))[1] = auth.uid()::text);

create policy "Owners delete their avatar assets"
  on storage.objects for delete to authenticated
  using (bucket_id = 'avatar-assets' and (storage.foldername(name))[1] = auth.uid()::text);
